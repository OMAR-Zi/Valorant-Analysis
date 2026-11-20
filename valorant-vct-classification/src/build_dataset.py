from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DATA_ROOT = WORKSPACE / "valorantchampiontour"
OUT = ROOT / "data" / "processed"
REPORT = ROOT / "data" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORT.mkdir(parents=True, exist_ok=True)

KEY = ["Tournament", "Stage", "Match Type", "Match Name", "Map"]
NUMERIC_PLAYER = [
    "Rating", "Average Combat Score", "Kills", "Deaths", "Assists",
    "Kills - Deaths (KD)", "Kill, Assist, Trade, Survive %",
    "Average Damage Per Round", "Headshot %", "First Kills",
    "First Deaths", "Kills - Deaths (FKD)"
]

def pct_number(value):
    if pd.isna(value):
        return np.nan
    s = str(value).strip().replace("%", "")
    try:
        return float(s)
    except ValueError:
        return np.nan

def clean_number(value):
    if pd.isna(value):
        return np.nan
    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return np.nan

def build_year(year):
    base = DATA_ROOT / f"vct_{year}"
    overview = pd.read_csv(base / "matches" / "overview.csv")
    scores = pd.read_csv(base / "matches" / "maps_scores.csv")
    ids = pd.read_csv(base / "ids" / "tournaments_stages_matches_games_ids.csv")

    overview["source_year"] = year
    both = overview.loc[overview["Side"] == "both"].copy()

    id_cols = KEY + ["Match ID", "Game ID"]
    id_map = ids[id_cols].drop_duplicates(KEY, keep="first")
    both = both.merge(id_map, on=KEY, how="left", validate="many_to_one")

    score_map = scores[KEY + ["Team A", "Team A Score", "Team B", "Team B Score"]].drop_duplicates(KEY, keep="first")
    both = both.merge(score_map, on=KEY, how="left", validate="many_to_one")

    for c in ["Team A Score", "Team B Score"]:
        both[c] = both[c].apply(clean_number)

    both["map_winner"] = np.where(
        both["Team A Score"] > both["Team B Score"], both["Team A"],
        np.where(both["Team B Score"] > both["Team A Score"], both["Team B"], np.nan)
    )

    # Maps are binary classification observations; exclude ties/no-result rows.
    keep_maps = both.loc[both["map_winner"].notna()].copy()

    # The map winner must exactly match a team name in the full-map overview.
    candidate = keep_maps.drop_duplicates(KEY)[KEY + ["map_winner"]]
    team_names = keep_maps[KEY + ["Team"]].drop_duplicates()
    verified = candidate.merge(team_names, on=KEY, how="inner", validate="many_to_many")
    verified = verified.loc[verified["map_winner"] == verified["Team"]]
    valid_keys = verified.drop_duplicates(KEY)[KEY]
    keep_maps = keep_maps.merge(valid_keys.assign(_valid=1), on=KEY, how="inner").drop(columns="_valid")

    for c in NUMERIC_PLAYER:
        if c in ("Kill, Assist, Trade, Survive %", "Headshot %"):
            keep_maps[c] = keep_maps[c].astype(str).str.replace("%", "", regex=False)
        keep_maps[c] = pd.to_numeric(keep_maps[c], errors="coerce")

    # Aggregate full-map player records to team-map level.
    agg = keep_maps.groupby(KEY + ["source_year", "Match ID", "Game ID", "Team"])
    team_rows = []
    for key_values, g in agg:
        row = dict(zip(KEY + ["source_year", "Match ID", "Game ID", "Team"], key_values))
        for c in NUMERIC_PLAYER:
            vals = g[c].dropna()
            row[f"team_{c}_mean"] = vals.mean() if len(vals) else np.nan
            row[f"team_{c}_sum"] = vals.sum() if len(vals) else np.nan

        agents = []
        for a in g["Agents"].dropna():
            agents.extend([x.strip().lower() for x in str(a).split(",") if x.strip()])
        counts = pd.Series(agents).value_counts() if agents else pd.Series(dtype="int64")
        row["composition_player_count"] = len(agents)
        row["agent_counts"] = counts.to_dict()
        team_rows.append(row)

    team = pd.DataFrame(team_rows)
    if team.empty:
        return team

    all_agents = sorted(set(a for d in team["agent_counts"] for a in d))
    for agent in all_agents:
        team[f"agent_{agent}"] = team["agent_counts"].apply(lambda d: int(d.get(agent, 0)))

    # Match-team pair and target.
    target_lookup = keep_maps[KEY + ["source_year", "map_winner", "Match ID", "Game ID"]].drop_duplicates(KEY)
    team = team.merge(target_lookup, on=KEY + ["source_year", "Match ID", "Game ID"], how="left", validate="many_to_one")
    team["win"] = (team["Team"] == team["map_winner"]).astype(int)

    # Attach opponent team features using the map key and team name.
    self_cols = [c for c in team.columns if c.startswith("team_") or c.startswith("agent_")]
    opp = team[KEY + ["source_year", "Match ID", "Game ID", "Team"] + self_cols].copy()
    opp = opp.rename(columns={"Team": "opponent_team"})
    opp = opp.rename(columns={c: c.replace("team_", "opponent_team_", 1) if c.startswith("team_") else c.replace("agent_", "opponent_agent_", 1) for c in opp.columns if c.startswith(("team_", "agent_"))})

    paired = team.merge(opp, on=KEY + ["source_year", "Match ID", "Game ID"], how="inner", suffixes=("", "_dup"))
    paired = paired.loc[paired["Team"] != paired["opponent_team"]].copy()

    # Relative numeric features (current team minus opponent).
    for c in NUMERIC_PLAYER:
        team_mean = f"team_{c}_mean"
        opp_mean = f"opponent_team_{c}_mean"
        if team_mean in paired.columns and opp_mean in paired.columns:
            paired[f"relative_{c}_mean"] = paired[team_mean] - paired[opp_mean]

    paired = paired.drop(columns=["agent_counts", "map_winner"])
    return paired


def audit_source_files():
    rows = []
    for year in range(2021, 2027):
        base = DATA_ROOT / f"vct_{year}"
        for subdir, name in [("matches", "overview.csv"), ("matches", "maps_scores.csv"), ("ids", "tournaments_stages_matches_games_ids.csv")]:
            p = base / subdir / name
            d = pd.read_csv(p)
            rows.append({"year": year, "file": str(p.relative_to(WORKSPACE)), "rows": len(d), "columns": len(d.columns), "bytes": p.stat().st_size})
    return pd.DataFrame(rows)

if __name__ == "__main__":
    source_audit = audit_source_files()
    source_audit.to_csv(REPORT / "source_file_audit.csv", index=False)

    pieces = [build_year(y) for y in range(2021, 2027)]
    df = pd.concat(pieces, ignore_index=True)

    df["map_key"] = df[KEY].astype(str).agg("|".join, axis=1) + "|" + df["source_year"].astype(str)
    df["match_key"] = df["Match ID"].astype(str)

    # Hard integrity assertions.
    assert df["win"].notna().all()
    assert set(df["win"].unique()).issubset({0, 1})
    assert not df[["Match ID", "Game ID", "Team"]].duplicated().any()

    map_counts = df.groupby("map_key")["win"].agg(["count", "sum"])
    invalid_pairs = map_counts[(map_counts["count"] != 2) | (map_counts["sum"] != 1)]
    if not invalid_pairs.empty:
        invalid_pairs.to_csv(REPORT / "invalid_map_pairs.csv")
        print("Invalid map pairs:", len(invalid_pairs))
        print(invalid_pairs.head(20).to_string())
    assert (map_counts["count"] == 2).all()
    assert (map_counts["sum"] == 1).all()

    df.to_csv(OUT / "vct_team_map_dataset.csv", index=False)

    # Concise audit report.
    numeric_missing = df.isna().sum().to_frame("missing_count")
    numeric_missing["missing_pct"] = numeric_missing["missing_count"] / len(df) * 100
    numeric_missing.to_csv(REPORT / "missing_values.csv")

    duplicate_key_count = df.duplicated(["Match ID", "Game ID", "Team"]).sum()
    map_summary = df.groupby("source_year").agg(
        team_map_rows=("win", "size"),
        maps=("map_key", "nunique"),
        matches=("Match ID", "nunique")
    ).reset_index()
    map_summary.to_csv(REPORT / "year_counts.csv", index=False)

    with open(REPORT / "construction_notes.md", "w") as f:
        f.write("# Data Construction Notes\n\n")
        f.write("- Source: local VCT 2021--2026 CSV files.\n")
        f.write("- Unit: one row per team per map.\n")
        f.write("- Filtering: only `Side == both` full-map player records.\n")
        f.write("- Target: map winner inferred by comparing verified Team A and Team B final map scores.\n")
        f.write("- Match grouping: `Match ID`; map traceability: `Game ID`.\n")
        f.write("- Team features: mean and sum of 12 full-map player statistics.\n")
        f.write("- Agent features: count of each agent selected in the five-player full-map composition.\n")
        f.write("- Opponent features: corresponding team-map statistics merged by match/map key.\n")
        f.write("- Excluded: final scores, win/loss outcome fields, winner label, and aggregate outcome-bearing agent tables from predictors.\n")
        f.write("- Team names and raw identifiers are metadata, not predictors.\n")

    print("Saved", len(df), "team-map rows and", df["map_key"].nunique(), "maps")
    print(map_summary.to_string(index=False))
