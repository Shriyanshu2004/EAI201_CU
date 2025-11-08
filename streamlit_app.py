"""
streamlit_app.py - very small Streamlit UI to run parts of the pipeline
Run: streamlit run streamlit_app.py from project root
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import joblib

BASE = Path(__file__).resolve().parents[0]
DATA_DIR = BASE / "data"
MODELS_DIR = BASE / "models"

st.title("FIFA Project Demo UI")

st.header("Current qualifiers (synthetic)")
q = pd.read_csv(DATA_DIR/"qualifiers.csv")
teams = pd.read_csv(DATA_DIR/"teams.csv")
cand = teams.merge(q, on="team_id")
st.dataframe(cand[cand.qualified==1].head(50))

st.header("Train models (demo)")
if st.button("Train"):
    import subprocess, sys
    subprocess.run([sys.executable, "src/train.py"])
    st.success("Training finished. Models saved.")

st.header("Predict finalists")
if st.button("Predict Top2"):
    m = joblib.load(MODELS_DIR / "rf_finalist.pkl")
    X = cand[cand.qualified==1][["fifa_ranking","team_name"]].copy().fillna(0)
    probs = m.predict_proba(X[["fifa_ranking"]])[:,1]
    X["prob"]=probs
    st.dataframe(X.sort_values("prob", ascending=False).head(5))
