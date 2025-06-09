from Enum import PlayerCategory
from sqlalchemy import Column, String
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional


class Jugador(SQLModel, table=True):
    sofifa_id: int = Field(default=None, primary_key=True)
    long_name: str = Field(..., min_length=2, max_length=70)
    age: int = Field(..., ge=16)
    nationality_name: str = Field(..., min_length=2, max_length=40)
    height_cm: float = Field(..., gt=0)
    club_name: Optional[str] = Field(default=None, min_length=2, max_length=40)
    player_positions: Optional[str] = Field(default=None, min_length=1, max_length=20)
    position_category: Optional[PlayerCategory] = Field(default=None)
    club_jersey_number: Optional[float] = Field(default=None, gt=0)
    is_active: Optional[bool] = Field(default=True)
    goals: Optional[int] = Field(default=None, ge=0)
    assists: Optional[int] = Field(default=None, ge=0)
    yellow_cards: Optional[int] = Field(default=None, ge=0)
    red_cards: Optional[int] = Field(default=None, ge=0)
    saved: Optional[int] = Field(default=None, ge=0)
    games: Optional[int] = Field(default=None, ge=0)
    saves: Optional[int] = Field(default=None, ge=0)
    goals_conceded: Optional[int] = Field(default=None, ge=0)
    clean_Sheets: Optional[int] = Field(default=None, ge=0)
    tackles: Optional[int] = Field(default=None, ge=0)
    interceptions: Optional[int] = Field(default=None, ge=0)
    fouls: Optional[int] = Field(default=None, ge=0)
    photo_url: Optional[str] = None
    nationality_flag_url: Optional[str] = None
    club_logo_url: Optional[str] = None



class Metricplayer(SQLModel, table=True):
    sofifa_id: int = Field(default=None, primary_key=True)
    long_name: str
    age: int
    nationality_name: str
    height_cm: int
    club_name: str
    player_positions: Optional[str] = None
    club_jersey_number: Optional[float] = Field(default=None, gt=0)
    overall: Optional[int]
    pace: Optional[float]
    shooting: Optional[float]
    defending: Optional[float]
    physical: Optional[float]
    power_shot: Optional[float]
    position_category: Optional[PlayerCategory]
    goalkeeping_diving: Optional[float]
    goalkeeping_handling: Optional[float]
    goalkeeping_kicking: Optional[float]
    goalkeeping_positioning: Optional[float]
    goalkeeping_reflexes: Optional[float]
    goalkeeping_speed: Optional[float]
    photo_url: Optional[str] = None
    nationality_flag_url: Optional[str] = None
    club_logo_url: Optional[str] = None
    is_active: bool = True

class MetricplayerPatchBody(BaseModel):
    club_jersey_number: Optional[float] = Field(default=None, gt=0)
    position_category: Optional[PlayerCategory] = None
    overall: Optional[float] = None
    pace: Optional[float] = None
    shooting: Optional[float] = None
    defending: Optional[float] = None
    physical: Optional[float] = None
    power_shot: Optional[float] = None
