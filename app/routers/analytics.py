from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics/league-table")
def league_table(db: Session = Depends(get_db)):

    teams = db.query(models.Team).all()
    matches = db.query(models.Match).all()

    table = {}

    for team in teams:
        table[team.id] = {
            "team": team.name,
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

    for match in matches:

        home = table[match.home_team_id]
        away = table[match.away_team_id]

        home["played"] += 1
        away["played"] += 1

        home["goals_for"] += match.home_goals
        home["goals_against"] += match.away_goals
        away["goals_for"] += match.away_goals
        away["goals_against"] += match.home_goals

        if match.home_goals > match.away_goals:
            home["wins"] += 1
            home["points"] += 3
            away["losses"] += 1

        elif match.home_goals < match.away_goals:
            away["wins"] += 1
            away["points"] += 3
            home["losses"] += 1

        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    for team in table.values():
        team["goal_difference"] = team["goals_for"] - team["goals_against"]

    sorted_table = sorted(
        table.values(),
        key = lambda x: (x["points"], x["goal_difference"], x["goals_for"]),
        reverse = True
    )

    return sorted_table