from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
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

@router.get("/analytics/top-scoring-teams")
def top_scoring_teams(db: Session = Depends(get_db)):

    teams = db.query(models.Team).all()
    matches = db.query(models.Match).all()

    goals = {team.id: {"team": team.name, "goals_scored": 0} for team in teams}

    for match in matches:

        if match.home_team_id in goals:
            goals[match.home_team_id]["goals_scored"] += match.home_goals

        if match.away_team_id in goals:
            goals[match.away_team_id]["goals_scored"] += match.away_goals

    sorted_goals = sorted(
        goals.values(),
        key=lambda x: x["goals_scored"],
        reverse=True
    )

    return sorted_goals

@router.get("/analytics/best-defence")
def best_defence(db: Session = Depends(get_db)):

    teams = db.query(models.Team).all()
    matches = db.query(models.Match).all()
    
    defence = {team.id: {"team": team.name, "goals_conceded": 0} for team in teams}

    for match in matches:

        if match.home_team_id in defence:
            defence[match.home_team_id]["goals_conceded"] += match.away_goals

        if match.away_team_id in defence:
            defence[match.away_team_id]["goals_conceded"] += match.home_goals

    sorted_defence = sorted(
        defence.values(),
        key=lambda x: x["goals_conceded"]
    )

    return sorted_defence

@router.get("/team-form/{team_id}")
def team_form(team_id: int, db: Session = Depends(get_db)):

    team = db.query(models.Team).filter(models.Team.id == team_id).first()

    if not team:
        raise HTTPException(status_code = 404, detail = "Team not found")

    matches = (
        db.query(models.Match)
        .filter(
            or_(
                models.Match.home_team_id == team_id,
                models.Match.away_team_id == team_id
            )
        )
        .order_by(models.Match.date.desc())
        .limit(5)
        .all()
    )

    results = []
    goals_for = 0
    goals_against = 0
    points = 0

    for match in matches:

        if match.home_team_id == team_id:
            gf = match.home_goals
            ga = match.away_goals
        else:
            gf = match.away_goals
            ga = match.home_goals

        goals_for += gf
        goals_against += ga

        if gf > ga:
            results.append("W")
            points += 3
        elif gf == ga:
            results.append("D")
            points += 1
        else:
            results.append("L")

    return {
        "team": team.name,
        "last_5_results": results,
        "points": points,
        "goals_for": goals_for,
        "goals_against": goals_against
    }