from typing import Optional
from Enum import PlayerCategory
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String
from pydantic import BaseModel


class Jugador(SQLModel, table=True):
    sofifa_id: int = Field(default=None, primary_key=True)
    long_name: str = Field(..., min_length=2, max_length=70)
    age: int = Field(..., ge=16)
    nationality_name: str = Field(..., min_length=2, max_length=40)
    height_cm: float = Field(..., gt=0)
    club_name: str = Field(..., min_length=2, max_length=40)
    position_category: Optional[PlayerCategory]
    club_jersey_number: float = Field(..., gt=0)



class JugadorPatchBody(BaseModel):
    club_name: Optional[str] = None
    club_jersey_number: Optional[float] = None
    position_category: Optional[PlayerCategory] = None


class Metricplayer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sofifa_id: int
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


class Estadisticas(SQLModel):
    goals: int = Field(..., ge=0)
    assists: int = Field(..., ge=0)
    yellow_cards: int = Field(..., ge=0)
    red_cards: int = Field(..., ge=0)
    saved: int = Field(..., ge=0)
    conceded: int = Field(..., ge=0)
