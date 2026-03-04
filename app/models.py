from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, unique = True, index = True)
    league = Column(String)
    country = Column(String)

    home_matches = relationship("Match", foreign_keys = "Match.home_team_id")
    away_matches = relationship("Match", foreign_keys = "Match.away_team_id")

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key = True, index = True)
    home_team_id = Column(Integer, ForeignKey("teams.id"))
    away_team_id = Column(Integer, ForeignKey("teams.id"))
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    date = Column(Date)
    competition = Column(String)