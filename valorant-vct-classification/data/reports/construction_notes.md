# Data Construction Notes

- Source: local VCT 2021--2026 CSV files.
- Unit: one row per team per map.
- Filtering: only `Side == both` full-map player records.
- Target: map winner inferred by comparing verified Team A and Team B final map scores.
- Match grouping: `Match ID`; map traceability: `Game ID`.
- Team features: mean and sum of 12 full-map player statistics.
- Agent features: count of each agent selected in the five-player full-map composition.
- Opponent features: corresponding team-map statistics merged by match/map key.
- Excluded: final scores, win/loss outcome fields, winner label, and aggregate outcome-bearing agent tables from predictors.
- Team names and raw identifiers are metadata, not predictors.
