# VCT Map Outcome Classification — Final Project Report

## 1. Research question

Can team performance statistics distinguish the winning and losing teams of a completed professional Valorant map?

This is **post-match classification**, not pre-match forecasting. Variables such as ACS, KAST, kills, deaths, ADR, rating, and final combat performance are recorded for or after the completed map.

## 2. Dataset and source

The project uses the local VCT 2021–2026 CSV collection. The complete raw source audit is in `data/reports/source_file_audit.csv`. The cleaned unit of observation is one team-map pair.

The reconstructed dataset contains 54,540 team-map rows and 27,270 maps. Year counts are in `data/reports/year_counts.csv`.

## 3. Construction and integrity

- Only full-map `Side == both` player records were retained.
- Attack-only and defend-only records were excluded to avoid counting players three times.
- Map winners were derived from verified Team A and Team B final map scores.
- A map was retained only when the map winner exactly matched a team name in the full-map overview.
- Tie rows and the two `01234`/`1234` unverifiable 2021 maps were excluded.
- Every valid map should contain exactly two team observations and one win label.
- `Match ID` is the grouping identifier; `Game ID` provides map traceability.

Construction details and exclusions are documented in `data/reports/construction_notes.md` and `data/reports/data_dictionary.md`.

## 4. EDA and missingness

Figures are saved in `outputs/figures/`:

- Target distribution
- Team-map observations by year
- Top missing-value features
- Selected performance distributions by outcome

The verified missingness report is `data/reports/missing_values.csv`. In the corrected numeric dataset, KAST is missing for 21.6062%, rating for 21.6685%, ACS for 0.1540%, and headshot percentage for 1.3495%. Statistical outlier counts and IQR bounds are in `outputs/tables/outlier_iqr_summary.csv`. Plausible extreme performances were retained rather than removed. The outlier audit is descriptive and is not used to delete valid observations.

## 5. Preprocessing and feature relevance

The corrected predictor set contains 119 columns and separates metadata and outcome fields from numeric and categorical features.

- `Match ID` and `Game ID` are excluded from predictors; `Match ID` is used only for grouping and `Game ID` only for map traceability.
- `win`, `map_winner`, Team A/B names, Team A/B scores, `map_key`, and `match_key` are excluded.
- Numeric features: median imputation and standardized scaling for logistic regression.
- Categorical context: most-frequent imputation and one-hot encoding.
- Random Forest: median imputation without scaling.
- Preprocessing is fitted inside each cross-validation training fold.

No SMOTE or resampling was used because the target has two effectively balanced team-map rows per map. Domain relevance analysis and opponent-relative features are used rather than unsafe complete-dataset feature selection.

## 6. Validation

A group-aware 20% held-out test split was created before tuning. `Match ID` was used as the group identifier. The held-out partition contains 43,622 training rows and 10,918 test rows. The split has zero overlapping match IDs.

A 4-fold shuffled `StratifiedGroupKFold` was applied to the training partition using scikit-learn 1.9.1. The canonical CV fold audit is `outputs/tables/cv_fold_audit.csv`. Every fold has zero overlap between its training and validation match groups.

## 7. Models

### Logistic Regression

A linear baseline using regularized probabilities. Hyperparameters tuned: `C`, `solver`, and optional balanced class weights.

### Random Forest

A nonlinear ensemble of decision trees. Hyperparameters tuned: number of trees, maximum depth, minimum leaf size, and maximum features.

## 8. Results — corrected identifier-audited experiment

| Model | CV mean F1 | CV std F1 | Test accuracy | Test precision | Test recall | Test F1 | Test ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.958415 | 0.002577 | 0.956036 | 0.956036 | 0.956036 | 0.956036 | 0.991780 |
| Random Forest | 0.955806 | 0.002825 | 0.953746 | 0.953497 | 0.954021 | 0.953759 | 0.992208 |

Logistic Regression has the stronger held-out accuracy and F1. Random Forest has the slightly higher ROC-AUC but does not provide enough measured improvement to override the interpretability advantage of Logistic Regression.

Corrected confusion matrices:

- Logistic Regression: TN 5,219; FP 240; FN 240; TP 5,219.
- Random Forest: TN 5,205; FP 254; FN 251; TP 5,208.

The original 126-column baseline remains archived in `outputs/tables/model_comparison.csv` and is not presented as the corrected or leakage-audited result. Its identifier-including metrics are retained only for comparison. The original and corrected test metrics differ only slightly after removing `Match ID` and `Game ID`.

Corrected charts, tables, models, and audit documentation are in `outputs/figures/`, `outputs/tables/`, and `outputs/models/`.

## 9. Limitations

- The task measures association in completed maps, not pre-match causation or forecasting.
- Tournament coverage and meta change across seasons.
- Missing or unavailable player fields vary across source records.
- Paired team rows are related and may share match-level context.
- A random match split may not measure future-season generalization.
- Relative performance features should not be interpreted as causal effects.
- The original 126-column baseline is not leakage-safe by its identifier audit and must not be used as the final reported result.
- The corrected run excludes `Match ID` and `Game ID`, while retaining `Match ID` only for grouping and `Game ID` only for traceability.


