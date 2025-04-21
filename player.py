from typing import Optional
from pydantic import BaseModel, Field

#Metricas jugador FIFA 2022
class Metricplayer (BaseModel):
    id: int
    overall : float
    pase : float
    shooting: float
    defending: float
    physical: float
    power_shot: float


#Modelo jugador FIFA
class PlayerF(BaseModel):
    id: int
    name:str = Field(..., min_length=2, max_length=70)
    age: int
    nationality: str = Field(..., min_length=2, max_length=40)
    team: str = Field(..., min_length=2, max_length=40)
    position: str = Field(..., min_length=2, max_length=40)