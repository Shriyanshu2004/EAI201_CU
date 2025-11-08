"""
etl.py - scraping and ETL helpers (template)
Fill in the real scraping logic where indicated.
"""
import pandas as pd
import time
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def load_teams():
    return pd.read_csv(DATA_DIR/"teams.csv")

def load_matches():
    return pd.read_csv(DATA_DIR/"matches.csv")

def summarize_team_form(team_id, matches_df, n=10):
    # compute recent winrate for a team
    m = matches_df[(matches_df.home_team_id==team_id) | (matches_df.away_team_id==team_id)]
    m = m.sort_values("date", ascending=False).head(n)
    wins = 0
    played = 0
    for _, r in m.iterrows():
        played += 1
        if r.winner_team_id == team_id:
            wins += 1
    return wins / played if played>0 else 0.0

# Placeholder for scraper - implement per-target site
def scrape_team_roster(team_fifa_code, save_raw=False):
    raise NotImplementedError("Replace with FBref or official site scraping code.")

if __name__ == "__main__":
    teams = load_teams()
    matches = load_matches()
    print("Teams:", len(teams))
    print("Matches:", len(matches))
    # demo: compute form for first 5 teams
    for tid in teams.team_id.head(5):
        print(tid, summarize_team_form(tid, matches))
