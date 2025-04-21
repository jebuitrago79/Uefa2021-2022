from typing import Optional
from pydantic import BaseModel, Field

# Modelo para las estadísticas del jugador (vida real y para arquero)
class Estadisticas(BaseModel):
    goals: int = Field(..., ge=0)
    assists: int = Field(..., ge=0)
    yellow_cards: int = Field(..., ge=0)
    red_cards: int = Field(..., ge=0)
    # Estadísticas de arquero
    saved: int = Field(..., ge=0)
    conceded: int = Field(..., ge=0)

# Modelo Jugador con estadísticas
class Jugador(BaseModel):
    sofifa_id: int
    long_name: str = Field(..., min_length=2, max_length=70)
    age: int = Field(..., ge=16)
    nationality_name: str = Field(..., min_length=2, max_length=40)
    height_cm: float = Field(..., gt=0)
    club_name: str = Field(..., min_length=2, max_length=40)
    player_positions: str = Field(..., min_length=2, max_length=40)
    club_jersey_number : float = Field(..., gt=0)
    stats: Estadisticas

class JugadorwithId(Jugador):
        pass