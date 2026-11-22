# VCT Map Outcome Classification

This project studies whether post-match team performance statistics distinguish a winning team from the losing team of a professional Valorant map.

## Important limitation

This is **post-match classification**, not pre-match prediction. It uses ACS, combat rating, kills, deaths, assists, ADR, KAST, and other statistics recorded during the map.

## Dataset

Downloaded from https://www.kaggle.com/datasets/ryanluong1/valorant-champion-tour-2021-2023-data. Unzip it in the project and name it valorantchampiontour. The source is reproduced in `data/reports/source_file_audit.csv`. The unit of analysis is one team-map observation. A valid map produces one win row and one loss row.

## Reproduce

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/build_dataset.py
python src/run_analysis.py
```

Run from the project directory.

## Outputs

- `data/processed/vct_team_map_dataset.csv`: reconstructed team-map dataset.
- `data/reports/`: source audit, year counts, missingness, construction notes.
- `outputs/figures/`: EDA, confusion-matrix, and ROC figures.
- `outputs/tables/`: model comparison, CV audit, and outlier summary.
- `outputs/models/`: final identifier-audited tuned estimators.
- `outputs/tables/original_model_comparison.csv`: preserved historical identifier-inclusive baseline for comparison.
- `outputs/tables/experiment_audit.json`: canonical experiment and grouping audit.
- `presentation/presentation_outline.md`: 10-minute presentation plan.

## Final experiment

The original baseline remains archived and must not be described as identifier-safe. The corrected experiment excludes `Match ID` and `Game ID` from `X`, uses `Match ID` only for grouping, and uses `Game ID` only for traceability. It reports Logistic Regression at 95.6036% test accuracy/F1 and Random Forest at 95.3746% test accuracy and 95.3759% test F1.

## Method

The construction filters to `Side == both`, aggregates only full-map player records, compares verified final map scores to derive `win`, creates agent composition counts, and pairs each team with its opponent. The corrected predictor matrix contains 119 columns; raw scores, winner fields, `Match ID`, and `Game ID` are excluded from predictors. Modeling uses a match-ID group-aware held-out test split and 4-fold `StratifiedGroupKFold` on the training partition.
