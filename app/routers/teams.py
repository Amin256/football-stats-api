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

@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team).all()
    return teams

@router.post("/teams")
def create_team(name: str, league: str, country: str, db: Session = Depends(get_db)):
    new_team = models.Team(name = name, league = league, country = country)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team