"""
train.py - train models on features.csv and save them under models/
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, precision_recall_fscore_support
import joblib

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "models"
MODELS_DIR.mkdir(exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_DIR/"features.csv")
    # simple filtering: use recent tournaments only for demo
    X = df.drop(columns=["team_id","tournament_year","label_finalist"])
    y = df.label_finalist
    return X, y

def train_and_evaluate():
    X, y = load_data()
    X = X.fillna(X.mean())
    # simple scaling + model
    rf = Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier(n_estimators=100, random_state=42))])
    lr = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=1000))])
    models = {"rf": rf, "lr": lr}
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    for name, m in models.items():
        aucs = []
        f1s = []
        for train_idx, test_idx in skf.split(X, y):
            m.fit(X.iloc[train_idx], y.iloc[train_idx])
            probs = m.predict_proba(X.iloc[test_idx])[:,1]
            preds = (probs >= 0.5).astype(int)
            aucs.append(roc_auc_score(y.iloc[test_idx], probs))
            p,r,f,_ = precision_recall_fscore_support(y.iloc[test_idx], preds, average='binary', zero_division=0)
            f1s.append(f)
        print(f"{name}: AUC mean={np.mean(aucs):.4f}, F1 mean={np.mean(f1s):.4f}")
        # fit on full data and save
        m.fit(X, y)
        joblib.dump(m, MODELS_DIR / f"{name}_finalist.pkl")
    print("Models trained and saved to models/")

if __name__ == "__main__":
    train_and_evaluate()
