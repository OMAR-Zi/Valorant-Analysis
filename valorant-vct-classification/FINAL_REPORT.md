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

The predictor set separates metadata and outcome fields from numeric and categorical features.

- Numeric features: median imputation and standardized scaling for logistic regression.
- Categorical context: most-frequent imputation and one-hot encoding.
- Random Forest: median imputation without scaling.
- Preprocessing is fitted inside each cross-validation training fold.

No SMOTE or resampling was used because the target has two effectively balanced team-map rows per map.

Domain relevance analysis and opponent-relative features are used rather than unsafe complete-dataset feature selection.

## 6. Validation

A group-aware 20% held-out test split was created before tuning. `Match ID` was used as the group identifier. A 4-fold `StratifiedGroupKFold` was applied to the training partition. The CV fold audit is `outputs/tables/cv_fold_audit.csv`.

No match ID crosses a fold's training and validation partition. The held-out match partition has zero overlapping match IDs with the training partition.

## 7. Models

### Logistic Regression

A linear baseline using regularized probabilities. Hyperparameters tuned: `C`, `solver`, and optional balanced class weights.

### Random Forest

A nonlinear ensemble of decision trees. Hyperparameters tuned: number of trees, maximum depth, minimum leaf size, and maximum features.

## 8. Results

| Model | CV mean F1 | CV std F1 | Test accuracy | Test precision | Test recall | Test F1 | Test ROC-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.958507 | 0.002680 | 0.955853 | 0.955853 | 0.955853 | 0.955853 | 0.991830 |
| Random Forest | 0.955550 | 0.002464 | 0.953013 | 0.953262 | 0.952739 | 0.953000 | 0.992125 |

Logistic Regression has the stronger held-out accuracy and F1, while Random Forest has a slightly higher ROC-AUC. The difference is small, so Logistic Regression is the simpler and more interpretable final baseline. Random Forest does not provide enough measured improvement to override that interpretability advantage in this experiment.

Confusion matrices and ROC curves are available in `outputs/figures/`. Tuned estimators are stored in `outputs/models/`.

## 9. Limitations

- The task measures association in completed maps, not pre-match causation or forecasting.
- Tournament coverage and meta change across seasons.
- Missing or unavailable player fields vary across source records.
- Paired team rows are related and may share match-level context.
- A random match split may not measure future-season generalization.
- Relative performance features should not be interpreted as causal effects.
