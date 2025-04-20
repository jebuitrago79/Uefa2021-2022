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
    id: int
    name: str = Field(..., min_length=2, max_length=70)
    age: int = Field(..., ge=16)
    nationality: str = Field(..., min_length=2, max_length=25)
    height: float = Field(..., gt=0)
    team: str = Field(..., min_length=2, max_length=25)
    position: str = Field(..., min_length=2, max_length=25)
    dorsal: int = Field(..., ge=1, le=99)
    goalkeeper: bool
    stats: Estadisticas

class JugadorwithId(Jugador):
        pass