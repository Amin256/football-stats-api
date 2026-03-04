from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/matches")
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).all()
    return matches

@router.post("/matches")
def create_match(
    home_team_id: int,
    away_team_id: int,
    home_goals: int,
    away_goals: int,
    competition: str,
    db: Session = Depends(get_db)
):

    new_match = models.Match(
        home_team_id = home_team_id,
        away_team_id = away_team_id,
        home_goals = home_goals,
        away_goals = away_goals,
        competition = competition
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return new_match