from typing import Optional
from pydantic import BaseModel, Field

class Metricplayer(BaseModel):
    sofifa_id: int
    long_name: str = Field(..., min_length=2, max_length=70)
    age: int = Field(..., ge=16)
    nationality_name: str = Field(..., min_length=2, max_length=40)
    height_cm: float = Field(..., gt=0)
    club_name: str = Field(..., min_length=2, max_length=40)
    player_positions: str = Field(..., min_length=2, max_length=40)
    club_jersey_number: float = Field(..., gt=0)
    overall: float
    pase: Optional[float] = None
    shooting: Optional[float] = None
    defending: Optional[float] = None
    physical: Optional[float] = None
    power_shot: Optional[float] = None

    class Config:
        from_attributes = True

