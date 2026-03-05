import pandas as pd
from datetime import datetime
from app.database import SessionLocal, engine
from app import models
from app.database import Base

Base.metadata.create_all(bind = engine)

DATASET_PATH = "data/premier_league_2023_2024.csv"

def import_dataset():

    db = SessionLocal()
    df = pd.read_csv(DATASET_PATH)

    teams = {}

    for _, row in df.iterrows():

        home_team = row["HomeTeam"]
        away_team = row["AwayTeam"]

        if home_team not in teams:
            team = models.Team(
                name = home_team,
                league = "Premier League",
                country = "England"
            )
            db.add(team)
            db.commit()
            db.refresh(team)
            teams[home_team] = team.id

        if away_team not in teams:
            team = models.Team(
                name = away_team,
                league = "Premier League",
                country = "England"
            )
            db.add(team)
            db.commit()
            db.refresh(team)
            teams[away_team] = team.id

    for _, row in df.iterrows():

        match = models.Match(
            home_team_id = teams[row["HomeTeam"]],
            away_team_id = teams[row["AwayTeam"]],
            home_goals = int(row["FTHG"]),
            away_goals = int(row["FTAG"]),
            competition = "Premier League",
            date = datetime.strptime(row["Date"], "%d/%m/%Y").date()
        )
        db.add(match)

    db.commit()
    db.close()

    print("Dataset imported successfully.")

if __name__ == "__main__":
    import_dataset()