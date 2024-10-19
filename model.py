from datetime import date
from typing import Optional

from pydantic import BaseModel


class FootballMatch(BaseModel):
    id: int
    home_team: str
    away_team: str
    match_date: date
    place: str
    duration: int
    home_score: int
    away_score: int
    yellow_cards: int
    red_cards: int


class MatchCreate(BaseModel):
    home_team: str
    away_team: str
    match_date: date
    place: str
    duration: int
    home_score: int
    away_score: int
    yellow_cards: int
    red_cards: int


class MatchUpdate(BaseModel):
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    match_date: Optional[date] = None
    place: Optional[str] = None
    duration: Optional[int] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    yellow_cards: Optional[int] = None
    red_cards: Optional[int] = None
