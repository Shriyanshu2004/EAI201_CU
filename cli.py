"""
cli.py - simple command line interface for common tasks
"""
import argparse
from pathlib import Path
import pandas as pd
from src.etl import load_teams
from src.train import train_and_evaluate
from src.predict import predict_top_k

BASE = Path(__file__).resolve().parents[0]
DATA_DIR = BASE / "data"

def add_qualifier(fifa_code):
    teams = pd.read_csv(DATA_DIR/"teams.csv")
    q = pd.read_csv(DATA_DIR/"qualifiers.csv")
    row = teams[teams.fifa_code==fifa_code]
    if row.empty:
        print("Team code not found. Add to teams.csv first.")
        return
    tid = int(row.team_id.values[0])
    if (q.fifa_code==fifa_code).any():
        q.loc[q.fifa_code==fifa_code, "qualified"] = 1
    else:
        q = q.append({"team_id":tid, "fifa_code":fifa_code, "qualified":1, "qualifier_date":"2025-11-01", "qualifier_source":"cli"}, ignore_index=True)
    q.to_csv(DATA_DIR/"qualifiers.csv", index=False)
    print(f"Marked {fifa_code} as qualified.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("train")
    p_add = sub.add_parser("add-qualifier")
    p_add.add_argument("fifa_code")
    p_pred = sub.add_parser("predict")
    p_pred.add_argument("--top", type=int, default=2)
    args = parser.parse_args()
    if args.cmd=="train":
        train_and_evaluate()
    elif args.cmd=="add-qualifier":
        add_qualifier(args.fifa_code)
    elif args.cmd=="predict":
        print(predict_top_k(args.top))
    else:
        parser.print_help()
