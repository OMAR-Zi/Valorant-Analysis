# Cahier des charges — Présentation PFE Valorant VCT

## Objectif

Create an approximately **10-minute academic project presentation**, first as **HTML**, then exportable to PDF and convertible to PowerPoint. The entire presentation must be written in **English**. The slides must be concise, professional, academic, and visually uncluttered.

Le style recherché correspond aux bonnes pratiques relevées dans des guides universitaires de soutenance : une idée principale par diapositive, des phrases courtes, des visuels utiles, une structure annoncée clairement et une progression visible. Il ne s’agit pas de copier une présentation existante ni de prétendre qu’un modèle précis a obtenu la mention « Très bien ».

## 1. Mandatory visual identity

- **Font: Arial everywhere**, including titles, captions, tables, charts, and slide numbers.
- **16:9** landscape format.
- White or very light grey background; black/charcoal text.
- One accent colour only: a restrained dark red inspired by Valorant.
- Consistent layout: identical margins, alignments, sizes, and element positions across slides.
- Generous whitespace; avoid unnecessary decoration, effects, and animations.
- Titles: approximately 28–34 pt; body text: 18–24 pt; sources and captions: at least 12–14 pt.
- Never shrink the font to fit more content; shorten the text instead.

## 2. Language, writing, and punctuation

- Use clear, natural, grammatically correct **English** throughout.
- Follow standard English punctuation: no space before commas, colons, semicolons, question marks, or exclamation marks; use consistent punctuation.
- Use consistent English section labels: “Introduction”, “Related Work”, “Proposed Approach”, “Experimental Study”, and “Conclusion & Future Work”.
- Avoid long sentences and paragraphs.
- Aim for **25–30 words maximum per slide**, excluding short source notes, and ideally 3–5 brief points.
- One main idea per slide.
- Ne pas mettre de point final après de simples mots-clés ; utiliser une ponctuation cohérente pour les phrases complètes.
- Slides should support the spoken presentation, not reproduce the written report.

## 3. Navigation, numbering, and progress

Chaque diapositive doit afficher clairement la partie du plan en cours, par exemple dans un bandeau discret en haut :

1. **INTRODUCTION**
2. **RELATED WORK**
3. **PROPOSED APPROACH**
4. **EXPERIMENTAL STUDY**
5. **CONCLUSION & FUTURE WORK**

Chaque page doit aussi comporter :
- Son numéro et le nombre total : `01 / 10`, `02 / 10`, etc.
- Une barre de progression discrète, cohérente avec le numéro réel.
- Le même emplacement pour ces éléments sur toutes les pages.

La page de garde est également numérotée, sauf consigne contraire de la faculté. Le plan doit rester visible dans l’indicateur de partie, sans répéter le plan complet sur chaque diapositive.

## 4. Recommended structure — 10 slides / 10 minutes

### 01 — Title slide
**Section: INTRODUCTION**

- Machine Learning Analysis of Professional Valorant Team Performance
- Classifying Match Outcomes at VCT Map Level
- Student names
- Supervisor
- Faculty of Sciences of Sfax — University of Sfax
- Academic year

Do not invent student names, supervisor details, logos, or academic year. Use a dominant title and discreet administrative details.

### 02 — Context and research question
**Section: INTRODUCTION**

Key points:
- Valorant: competitive esports
- Detailed performance statistics
- ACS, ADR, K/D, KAST

Highlight the central research question:

> Can the winning team be identified from its recorded performance statistics during a professional map?

### 03 — Objectives and workflow
**Section: INTRODUCTION**

- Build a clean, usable dataset
- Explore performance features
- Train two classification models
- Compare model performance

Schéma horizontal : **Données → Préparation → Modélisation → Évaluation**

### 04 — Related work
**Section: RELATED WORK**

Cover only the concepts needed:
- Supervised learning
- Binary classification
- Logistic regression
- Random Forest

Comparer les deux modèles en deux colonnes, avec une explication très courte pour chacun. Pas de longs développements théoriques.

### 05 — Dataset
**Section: EXPERIMENTAL STUDY**

Afficher les informations calculées sur le dataset final :
- Source: VCT dataset from Kaggle
- Actual date range
- Number of maps
- Number of team-map observations
- Number of selected features
- Target: `win` (1 = win, 0 = loss)

Utiliser de grands chiffres et de courtes étiquettes. **Do not reuse previously stated statistics without recalculating them from the exact dataset used in the final experiment.**

### 06 — Data preparation and exploration
**Section: PROPOSED APPROACH**

- Filter valid observations
- Handle missing values
- Check for duplicates
- Construct agent-composition features
- Remove data-leakage features

Include one real, readable chart: target distribution, missing-value overview, or a comparison of a statistic between winners and losers. Do not use decorative charts or fabricated data.

### 07 — Methodology and models
**Section: PROPOSED APPROACH**

Schéma : **Données nettoyées → Prétraitement → Validation groupée → Modèles → Évaluation**

Models:
- Logistic regression
- Random Forest

Key point: both teams from the same map must remain in the same validation group.

### 08 — Experimental protocol and metrics
**Section: EXPERIMENTAL STUDY**

- Train/test split
- Four-fold cross-validation grouped by match, if this is the configuration actually used
- Hyperparameter tuning on the training set
- Final evaluation on the independent test set

Métriques :
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Show metrics as short labels or restrained visual markers, not paragraphs of definitions.

### 09 — Results and discussion
**Section: EXPERIMENTAL STUDY**

- Model comparison table
- Confusion matrix for the best model
- One key interpretation
- One important limitation

Tableau à compléter uniquement avec les résultats calculés :

| Modèle | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic regression | To be calculated | To be calculated | To be calculated | To be calculated | To be calculated |
| Random Forest | To be calculated | To be calculated | To be calculated | To be calculated | To be calculated |

Never invent or estimate results. Replace all placeholders with actual measured results before the presentation.

### 10 — Conclusion and future work
**Section: CONCLUSION & FUTURE WORK**

Conclusion :
- Answer to the research question
- Best-performing model based on actual results
- Main contribution

Perspectives :
- Evaluate additional models
- Study changes in agents and strategies
- Extend the work towards genuine pre-match prediction

End with “Thank you for your attention” and “Questions”.

## 5. Scientific accuracy: mandatory requirements

The project uses statistics recorded **during or after a completed map**, such as ACS, kills, deaths, assists, ADR, KAST, and rating.

The current task is therefore **post-match classification**, not prediction of the winner before the match.

Correct wording:

> Classifying the winning team using performance statistics recorded during a completed professional map.

Do not describe this as “predicting the winner before the match starts.”

### Preventing data leakage

Do not use the following as predictive features:
- La cible `win`
- Le nom ou l’identifiant du vainqueur
- Le score final, les manches gagnées/perdues ou leur différence
- Toute variable directement dérivée du résultat final
- Des agrégats de victoires/défaites qui incluent la carte évaluée

Keep match and map identifiers for grouping and auditing, but do not use them as predictive features. The two team-map observations from the same map must remain in the same group and the same split.


## 6. Integrating all relevant project outputs into the presentation

The presentation must use **relevant outputs actually produced by the project**, not just images. The HTML author must inspect the completed project, its generated files, notebooks, scripts, evaluation reports, and saved results, then select the evidence that best supports the original presentation structure.

Do not assume that every item listed below exists. Include an item only if the project has genuinely produced it and it helps explain the work. Do not create artificial outputs merely to fill a slide.

### General selection principle

For every section of the presentation, ask:

1. What does the audience need to understand at this point?
2. Which actual project output provides evidence for that point?
3. Can it be communicated more clearly as a chart, compact table, diagram, key number, or short statement?
4. Is the output methodologically valid and consistent with the final experiment?

Prefer a small number of high-value outputs over a large collection of screenshots. Never add raw terminal screenshots, code screenshots, full notebook screenshots, or entire CSV previews unless there is a compelling reason. Recreate useful information as clean presentation-quality visuals.

### Output types to consider

Inspect the project for the following types of outputs and use those that are available and relevant:

**Dataset and data preparation**
- Dataset source, date range, number of maps, observations, teams, and selected features.
- Dataset schema or a concise feature-group summary.
- Before/after cleaning counts, if recorded and meaningful.
- Missing-value analysis.
- Duplicate and invalid-record checks.
- Target-class distribution.
- Team-map construction validation, such as two team observations per map and one winner per map.
- Agent-composition summaries.
- Data-quality audit results.

**Exploratory data analysis**
- Distributions of relevant numeric features.
- Comparisons of performance statistics between winning and losing teams.
- Correlation analysis, where interpretable.
- Agent-pick or agent-composition frequencies.
- Trends by year, tournament, map, or other context, if they support the research question.
- Outlier analysis, with a distinction between data errors and legitimate extreme performances.

**Methodology and implementation**
- A diagram of the actual data-processing and modelling pipeline.
- The final feature groups and target definition.
- Preprocessing choices actually implemented.
- Feature-selection results, if feature selection was performed.
- Cross-validation and train/test split design.
- Hyperparameter search results, if tuning was performed.
- A concise explanation of how match-level grouping prevents related team observations from leaking across splits.

**Experimental results**
- Cross-validation scores and variability.
- Independent test-set metrics.
- Model-comparison tables.
- Confusion matrices.
- ROC curves and AUC, if probability estimates are available.
- Precision-recall curves, if useful for the class balance and evaluation.
- Classification reports.
- Threshold analysis, if performed.
- Runtime or training-cost comparison, if relevant.

**Interpretation and discussion**
- Feature importance or permutation importance, if computed correctly.
- Logistic Regression coefficients, interpreted with care and in the context of scaling and encoding.
- Error analysis: examples or patterns of false positives and false negatives, without exposing irrelevant raw records.
- Differences in model behaviour.
- Limitations revealed by the dataset or experiments.

### Map project outputs to the original presentation structure

Keep the user's original five-part structure:

1. Introduction
2. Related Work
3. Proposed Approach
4. Experimental Study
5. Conclusion & Future Work

Use project outputs as evidence within the appropriate section:

| Presentation section | What to explain | Relevant project outputs to consider |
|---|---|---|
| **Introduction** | Context, problem, objective | One concise motivating statistic or example only if it genuinely helps; research question and objective |
| **Related Work** | Concepts and methods behind the approach | A compact comparison of the selected algorithms and evaluation concepts; use cited academic or authoritative sources rather than project-generated claims |
| **Proposed Approach** | The solution and workflow | Data-cleaning summary, feature groups, target construction, preprocessing pipeline, feature-selection output, workflow diagram, validation design |
| **Experimental Study** | Data, metrics, experiments, results | Dataset statistics, EDA charts, data-quality checks, hyperparameter results, cross-validation scores, test metrics, model comparison, confusion matrices, ROC/PR curves, feature interpretation |
| **Conclusion & Future Work** | What was learned and what remains | Best verified result, main finding, key limitation, and realistic future improvements |

The table is a selection guide, not a requirement to place every listed item on the slides.

### Suggested 10-slide placement

- **Slide 01 — Title:** project title and academic details; no analytical output required.
- **Slide 02 — Context and research question:** concise motivation and the central question; use at most one supporting statistic if useful and verified.
- **Slide 03 — Objectives and workflow:** project objectives and a simple overview diagram.
- **Slide 04 — Related work:** concise algorithm comparison and relevant references; do not insert arbitrary project charts here.
- **Slide 05 — Dataset:** verified dataset statistics, target definition, and a compact data-quality or dataset overview output.
- **Slide 06 — Data preparation and exploration:** actual cleaning evidence and the most informative EDA charts.
- **Slide 07 — Proposed methodology and models:** actual pipeline, feature groups, preprocessing, and group-aware validation design.
- **Slide 08 — Experimental protocol:** actual split strategy, cross-validation setup, tuning summary, and evaluation metrics.
- **Slide 09 — Results and discussion:** actual model comparison, confusion matrix, ROC/PR curve if available, and one useful interpretation or error-analysis result.
- **Slide 10 — Conclusion and future work:** strongest verified finding, limitations, and realistic next steps.

If the project produces an important output that does not fit without overcrowding, either omit it from the main presentation or add a small appendix slide only when it is essential for answering likely jury questions. Keep the main presentation within approximately 10–11 slides unless the user explicitly requests otherwise.

### Requirements for all inserted outputs

- Use the final, executed project outputs, not fabricated examples or placeholder values.
- Check that each result corresponds to the final dataset, final target, final feature set, and final model run.
- Do not mix results from different train/test splits or different experiment versions.
- Distinguish cross-validation results from independent test-set results.
- Label metrics clearly and state whether values are percentages, decimals, or counts.
- Use consistent rounding throughout the presentation.
- Add concise captions where the meaning is not immediately obvious.
- Every chart, table, and statistic must have a clear purpose in the argument.
- Translate all titles, labels, legends, captions, and annotations into English.
- Recreate tables and charts cleanly in HTML/CSS or as high-resolution assets; do not paste unreadable screenshots.
- Include source notes for external data or references where appropriate.
- Do not imply causation from feature importance or correlations.
- Do not present a feature as predictive if it leaks the outcome or would not be available at the claimed prediction time.

### Missing outputs and unfinished project work

If the project has not yet generated a needed result:
- Do not invent it.
- Do not silently substitute a different result.
- Mark it as “Not yet generated” in the working draft or omit it from the final slides.
- Identify the exact script, notebook, or experiment that must be run to produce it, if this can be determined from the project.
- Keep the final presentation honest about what has and has not been completed.

### Reproducibility and asset handling

- Keep generated charts, tables, and exported result files in a clear project output folder.
- Preserve the scripts or notebook cells that generated them.
- Use correct relative paths from the HTML file to any external images or data assets.
- Ensure all assets remain available when the HTML is opened, printed, or converted to PDF.
- If a result is easier to render directly as HTML (for example, a compact table or workflow diagram), do so rather than exporting an unnecessary image.
- The HTML must not depend on a live Python session or external service to display saved results.

Example organisation (adapt to the actual project):

```text
project/
├── data/
├── notebooks/
├── src/
├── outputs/
│   ├── figures/
│   ├── tables/
│   ├── metrics/
│   ├── reports/
│   └── logs/
└── presentation/
    ├── presentation.html
    └── assets/
```

Do not create empty folders or fake files merely to match this example.

## 7. HTML and export requirements

Le HTML doit être autonome, avec CSS intégré, sans dépendance à une police distante ou à un script externe.

Exigences :
- `font-family: Arial, Helvetica, sans-serif`
- Une page HTML par diapositive
- Dimensions 16:9 paysage
- Numéro, partie courante et progression sur chaque page
- Sauts de page contrôlés
- Couleurs préservées à l’impression
- Aucun contenu coupé ou débordant
- Graphiques et tableaux lisibles après export PDF

Recommended CSS starting point:

```css
@page {
  size: 13.333in 7.5in;
  margin: 0;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  color: #171717;
  background: #eeeeee;
}

.slide {
  width: 13.333in;
  height: 7.5in;
  position: relative;
  overflow: hidden;
  page-break-after: always;
  break-after: page;
  background: #ffffff;
  padding: 0.55in 0.7in 0.6in;
}

.slide:last-child {
  page-break-after: auto;
  break-after: auto;
}

@media screen {
  .slide {
    margin: 24px auto;
    box-shadow: 0 2px 14px rgba(0, 0, 0, 0.12);
  }
}

@media print {
  body {
    background: #ffffff;
    print-color-adjust: exact;
    -webkit-print-color-adjust: exact;
  }

  .slide {
    margin: 0;
    box-shadow: none;
  }
}
```

Inspect the exported PDF page by page: CSS alone cannot guarantee that every browser or converter will avoid overflow.

## 8. Reference guidance

Ces ressources servent à guider la structure et les bonnes pratiques. Elles ne prouvent pas qu’une présentation précise a obtenu la mention « Très bien ».

- **UPSAT — Support de soutenance PFE** : recommande Arial, une police homogène, la numérotation des diapositives (hors page de garde dans ses consignes) et une progression allant de l’introduction aux résultats, puis à la conclusion.  
  https://upsat.tn/wp-content/uploads/2025/12/soutenance-PFE-1-compresse.pdf

- **ISEAHM — Guide PFE 2025–2026** : recommande des diapositives lisibles, peu de texte, des phrases courtes et une idée majeure par diapositive ; le guide donne 25 mots comme repère.  
  https://iseahm.rnu.tn/userfiles/files/GIDE%20PFE%20ISEAHM%202025-2026.pdf

- **ESCT — Guide d’élaboration de PFE** : rappelle que les règles de présentation PowerPoint font partie des consignes académiques à respecter.  
  https://esct.rnu.tn/fr/vie-estudiantine/informations-etudiants/memoires-pfe/guide-d-elaboration-de-pfe

- **Université de Tlemcen — Conseils pour le discours et le diaporama de soutenance** : insiste sur la hiérarchisation de l’information, une idée par diapositive et l’articulation entre support visuel et présentation orale.  
  https://elearn.univ-tlemcen.dz/mod/page/view.php?id=91652

## 9. Final quality checklist

- [ ] Environ 10 diapositives pour 10 minutes
- [ ] Une idée principale par diapositive
- [ ] Texte bref et lisible à distance
- [ ] Arial partout
- [ ] English grammar, spelling, and punctuation checked
- [ ] Numéro de page sur chaque diapositive
- [ ] Current section visible on every slide
- [ ] Barre de progression cohérente
- [ ] Format 16:9 paysage
- [ ] Une page PDF par diapositive
- [ ] Aucun titre, graphique ou tableau coupé
- [ ] All figures and results verified against the final experiment
- [ ] Post-match classification clearly distinguished from pre-match prediction
- [ ] Data and visual sources acknowledged
- [ ] Exported PDF reviewed page by page

## Expected deliverable

An approximately 10-slide HTML presentation, written entirely in English, with a restrained and consistent design, minimal text, Arial typography, slide numbering, a persistent current-section indicator, and actual project-generated figures. All content and results must match the executed project.
