"""
features.py - functions to build features for model training and prediction
"""
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def build_features_snapshot(tournament_year, teams_df=None, matches_df=None):
    teams = teams_df if teams_df is not None else pd.read_csv(DATA_DIR/"teams.csv")
    matches = matches_df if matches_df is not None else pd.read_csv(DATA_DIR/"matches.csv")
    rows = []
    for _, t in teams.iterrows():
        tid = t.team_id
        # simple example features from teams.csv + random-ish placeholders
        avg_age = 27.0
        last10_winrate = 0.5
        goal_diff_20 = 0
        avg_caps = 30
        pct_top5 = 0.1
        wc_apps = 0
        rows.append({
            "team_id": tid, "tournament_year": tournament_year, "avg_age": avg_age,
            "last10_winrate": last10_winrate, "goal_diff_20": goal_diff_20,
            "avg_caps": avg_caps, "pct_top5_league": pct_top5, "wc_apps_last5": wc_apps,
            "fifa_ranking": t.fifa_ranking, "label_finalist": 0
        })
    out = pd.DataFrame(rows)
    return out

if __name__ == "__main__":
    df = build_features_snapshot(2026)
    print(df.head())
    df.to_csv(DATA_DIR/"features_2026_snapshot.csv", index=False)
