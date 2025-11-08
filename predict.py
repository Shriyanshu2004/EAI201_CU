"""
predict.py - load model and predict finalists for current candidate teams
"""
import pandas as pd
from pathlib import Path
import joblib

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "models"

def load_candidates():
    # by default use qualifiers.csv (currently qualified) + simulated if present
    q = pd.read_csv(DATA_DIR/"qualifiers.csv")
    teams = pd.read_csv(DATA_DIR/"teams.csv")
    cand = teams.merge(q, on="team_id")
    # filter qualified==1 or simulated file
    cand = cand[cand.qualified==1].copy()
    return cand

def prepare_features(candidates_df):
    # minimal feature set for demo: take fifa_ranking and simple placeholders
    X = candidates_df[["team_id","fifa_code","team_name","fifa_ranking"]].copy()
    X_num = X[["fifa_ranking"]].copy().fillna(X.fifa_ranking.mean())
    return X_num, X

def predict_top_k(k=2, model_name="rf"):
    X_num, Xmeta = prepare_features(load_candidates())
    model = joblib.load(MODELS_DIR / f"{model_name}_finalist.pkl")
    probs = model.predict_proba(X_num)[:,1]
    Xmeta["prob_finalist"] = probs
    return Xmeta.sort_values("prob_finalist", ascending=False).head(k)

if __name__ == "__main__":
    print(predict_top_k(2))
