from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedGroupKFold, GroupShuffleSplit, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, ConfusionMatrixDisplay,
                             RocCurveDisplay)
import joblib

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "vct_team_map_dataset.csv"
FIG = ROOT / "outputs" / "figures"
TABLE = ROOT / "outputs" / "tables"
MODEL = ROOT / "outputs" / "models"
for p in (FIG, TABLE, MODEL): p.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid")
np.random.seed(42)

df = pd.read_csv(DATA)

# EDA and audit figures.
plt.figure(figsize=(7,4))
sns.countplot(data=df, x="win", palette=["#c44e52", "#4c72b0"])
plt.xticks([0,1],["Loss","Win"])
plt.title("Team-map target distribution")
plt.xlabel("Outcome"); plt.ylabel("Observations")
plt.tight_layout(); plt.savefig(FIG/"01_target_distribution.png", dpi=160); plt.close()

plt.figure(figsize=(9,4))
year_counts = df.groupby("source_year")["win"].size()
year_counts.plot(kind="bar", color="#4c72b0")
plt.title("Team-map observations by year")
plt.xlabel("Year"); plt.ylabel("Team-map rows")
plt.tight_layout(); plt.savefig(FIG/"02_observations_by_year.png", dpi=160); plt.close()

missing = df.isna().mean().mul(100).sort_values(ascending=False).head(15)
plt.figure(figsize=(9,5))
missing.plot(kind="barh", color="#dd8452")
plt.gca().invert_yaxis()
plt.title("Top missing-value percentages")
plt.xlabel("Missing (%)")
plt.tight_layout(); plt.savefig(FIG/"03_missing_values.png", dpi=160); plt.close()

numeric_candidates = [c for c in df.columns if c.startswith("team_") and c.endswith("_mean")]
selected = [c for c in numeric_candidates if c in [
    "team_Rating_mean","team_Average Combat Score_mean","team_Kills_mean",
    "team_Deaths_mean","team_Average Damage Per Round_mean"
]]
if selected:
    plot_df = df.melt(id_vars="win", value_vars=selected, var_name="feature", value_name="value")
    g = sns.displot(plot_df, x="value", hue="win", col="feature", col_wrap=3,
                    kind="kde", common_norm=False, fill=True, height=3, aspect=1.3)
    g.set_titles("{col_name}"); g.set_axis_labels("Feature value", "Density")
    g.fig.suptitle("Selected team performance distributions by outcome", y=1.02)
    g.savefig(FIG/"04_performance_distributions.png", dpi=160)

# IQR outlier summary for numeric team/opponent/relative means.
outlier_rows=[]
for c in [c for c in df.select_dtypes(include=np.number).columns
          if c.startswith(("team_", "opponent_team_", "relative_"))]:
    vals=df[c].dropna()
    if len(vals)==0: continue
    q1,q3=vals.quantile([.25,.75]); iqr=q3-q1
    lo,hi=q1-1.5*iqr,q3+1.5*iqr
    n=int(((vals<lo)|(vals>hi)).sum())
    if n:
        outlier_rows.append({"feature":c,"outlier_count":n,"outlier_pct":100*n/len(vals),"lower_bound":lo,"upper_bound":hi})
outlier_df=pd.DataFrame(outlier_rows).sort_values("outlier_pct",ascending=False)
outlier_df.to_csv(TABLE/"outlier_iqr_summary.csv",index=False)

# Separate predictor features from metadata and leakage fields.
metadata = {"win","map_key","match_key","Team","opponent_team","map_winner",
            "Match Name","Team A","Team B","Team A Score","Team B Score",
            "composition_player_count","agent_counts"}
exclude_prefix = ("Team A", "Team B")
feature_cols = [c for c in df.columns if c not in metadata and not c.startswith(exclude_prefix)]
cat_cols = [c for c in ["Tournament","Stage","Match Type","source_year","Map"] if c in feature_cols]
num_cols = [c for c in feature_cols if c not in cat_cols and pd.api.types.is_numeric_dtype(df[c])]

X=df[feature_cols].copy(); y=df["win"].astype(int); groups=df["Match ID"].astype(str)

# Group-aware held-out test split.
gss=GroupShuffleSplit(n_splits=1,test_size=.20,random_state=42)
train_idx,test_idx=next(gss.split(X,y,groups=groups))
X_train=X.iloc[train_idx]; X_test=X.iloc[test_idx]
y_train=y.iloc[train_idx]; y_test=y.iloc[test_idx]
groups_train=groups.iloc[train_idx]; groups_test=groups.iloc[test_idx]
assert set(groups_train).isdisjoint(set(groups_test))

cv=StratifiedGroupKFold(n_splits=4,shuffle=True,random_state=42)
cv_splits=list(cv.split(X_train,y_train,groups=groups_train))
for fold,(tr,va) in enumerate(cv_splits,1):
    tr_g=set(groups_train.iloc[tr]); va_g=set(groups_train.iloc[va])
    assert tr_g.isdisjoint(va_g)

numeric_pipe=Pipeline([("imputer",SimpleImputer(strategy="median")),("scaler",StandardScaler())])
categorical_pipe=Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),
                           ("onehot",OneHotEncoder(handle_unknown="ignore"))])
preprocessor=ColumnTransformer([("num",numeric_pipe,[c for c in num_cols if c in X_train.columns]),
                                ("cat",categorical_pipe,[c for c in cat_cols if c in X_train.columns])])

log_pipe=Pipeline([("preprocess",preprocessor),("model",LogisticRegression(max_iter=2000,random_state=42))])
log_grid={"model__C":[0.1,1.0,10.0],"model__solver":["liblinear"],"model__class_weight":[None,"balanced"]}
log=GridSearchCV(log_pipe,log_grid,cv=cv_splits,scoring="f1",n_jobs=-1,return_train_score=True)
log.fit(X_train,y_train)

rf_num_pipe=Pipeline([("imputer",SimpleImputer(strategy="median"))])
rf_pre=ColumnTransformer([("num",rf_num_pipe,[c for c in num_cols if c in X_train.columns]),
                          ("cat",categorical_pipe,[c for c in cat_cols if c in X_train.columns])])
rf_pipe=Pipeline([("preprocess",rf_pre),("model",RandomForestClassifier(random_state=42,n_jobs=-1))])
rf_grid={"model__n_estimators":[200],"model__max_depth":[12,None],"model__min_samples_leaf":[1,2],"model__max_features":["sqrt"]}
rf=GridSearchCV(rf_pipe,rf_grid,cv=cv_splits,scoring="f1",n_jobs=-1,return_train_score=True)
rf.fit(X_train,y_train)

results=[]
for name,search in [("Logistic Regression",log),("Random Forest",rf)]:
    pred=search.predict(X_test)
    prob=search.predict_proba(X_test)[:,1]
    metrics={"Model":name,"CV mean F1":search.best_score_,
             "CV std F1":search.cv_results_["std_test_score"][search.best_index_],
             "Test accuracy":accuracy_score(y_test,pred),"Test precision":precision_score(y_test,pred),
             "Test recall":recall_score(y_test,pred),"Test F1":f1_score(y_test,pred),
             "Test ROC-AUC":roc_auc_score(y_test,prob),"Best parameters":str(search.best_params_)}
    results.append(metrics)

    cm=confusion_matrix(y_test,pred)
    disp=ConfusionMatrixDisplay(cm,display_labels=["Loss","Win"])
    disp.plot(cmap="Blues",values_format="d")
    plt.title(f"{name}: Confusion Matrix")
    plt.tight_layout(); plt.savefig(FIG/(name.lower().replace(" ","_")+"_confusion_matrix.png"),dpi=160); plt.close()

    RocCurveDisplay.from_predictions(y_test,prob)
    plt.title(f"{name}: ROC Curve")
    plt.tight_layout(); plt.savefig(FIG/(name.lower().replace(" ","_")+"_roc.png"),dpi=160); plt.close()

comparison=pd.DataFrame(results)
comparison.to_csv(TABLE/"model_comparison.csv",index=False)
pd.DataFrame({"fold":[i+1 for i in range(4)],
              "train_rows":[len(tr) for tr,va in cv_splits],
              "validation_rows":[len(va) for tr,va in cv_splits],
              "train_matches":[groups_train.iloc[tr].nunique() for tr,va in cv_splits],
              "validation_matches":[groups_train.iloc[va].nunique() for tr,va in cv_splits]}).to_csv(TABLE/"cv_fold_audit.csv",index=False)

joblib.dump(log.best_estimator_,MODEL/"logistic_regression.joblib")
joblib.dump(rf.best_estimator_,MODEL/"random_forest.joblib")

print(comparison.to_string(index=False))
print("Train/test match overlap:", bool(set(groups_train) & set(groups_test)))
print("Matched train/test match overlap count:", len(set(groups_train) & set(groups_test)))
print("Predictor count:",len(feature_cols))
