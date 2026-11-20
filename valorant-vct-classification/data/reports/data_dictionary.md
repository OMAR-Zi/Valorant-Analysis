# Data Dictionary

## Source and unit

- Source: local `valorantchampiontour/vct_2021` through `vct_2026` CSV files.
- Unit: one team-map observation.
- Target: `win`, where 1 is the team that won the map and 0 is the opposing team.
- Group: `Match ID` is used for group-aware splitting. `Game ID` identifies the map.

## Key metadata

- `Tournament`, `Stage`, `Match Type`, `Match Name`, `Map`: map/tournament context.
- `source_year`: 2021–2026 source year.
- `Match ID`: match-level grouping identifier.
- `Game ID`: map identifier.
- `Team`: current team represented by the row.
- `opponent_team`: opposing team represented by the same map.
- `map_key`: audit key combining match context, map, and year.

## Target

- `win`: binary target derived by comparing the row team against the map winner. It is never included as a predictor.

## Team performance features

For each full-map numeric player statistic:

- `team_<statistic>_mean`: mean across the team's five full-map player records.
- `team_<statistic>_sum`: sum across the team's full-map player records.
- `opponent_team_<statistic>_mean/sum`: corresponding opponent aggregate.
- `relative_<statistic>_mean`: team mean minus opponent mean.

Included source statistics are Rating, Average Combat Score, Kills, Deaths, Assists, K/D, KAST, ADR, Headshot %, First Kills, First Deaths, and FKD.

## Agent composition

- `agent_<agent>`: number of current-team players selecting the agent on this map.
- `opponent_agent_<agent>`: corresponding opponent composition count.
- `composition_player_count`: number of player-agent selections represented in the composition audit.

## Leakage exclusions

The following are metadata or outcome fields and are excluded from `X`:

- `win`
- `map_winner`
- `Team A`, `Team B`, `Team A Score`, `Team B Score`
- Raw match/team identifiers used for traceability only
- Aggregate win/loss columns from `teams_picked_agents.csv`

The primary model uses no direct or score-derived outcome field as a predictor.
