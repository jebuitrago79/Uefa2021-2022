from typing import Optional
from pydantic import BaseModel, Field


class Estadisticas(BaseModel):
    goals: int = Field(..., ge=0)
    assists: int = Field(..., ge=0)
    yellow_cards: int = Field(..., ge=0)
    red_cards: int = Field(..., ge=0)
    saved: int = Field(..., ge=0)
    conceded: int = Field(..., ge=0)


class Jugador(BaseModel):
    sofifa_id: int
    long_name: str = Field(..., min_length=2, max_length=70)
    age: int = Field(..., ge=16)
    nationality_name: str = Field(..., min_length=2, max_length=40)
    height_cm: float = Field(..., gt=0)
    club_name: str = Field(..., min_length=2, max_length=40)
    position_category: PlayerCategory = Field(sa_column=Column(String))
    club_jersey_number: float = Field(..., gt=0)


class Config:
    from_attributes = True