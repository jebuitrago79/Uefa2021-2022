from database import sync_engine
from sqlmodel import Session, select
from models_sqlmodel import Metricplayer
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

router = APIRouter()
templates = Jinja2Templates(directory="templates")

df_imagenes = pd.read_csv("Jugadores_2021_22.csv")

@router.get("/players", response_class=HTMLResponse)
def list_players(request: Request):
    with Session(sync_engine) as session:  # ✅ usar sync_engine
        jugadores = session.exec(select(Metricplayer)).all()

    enriched_players = []
    for j in jugadores:
        match = df_imagenes[df_imagenes["sofifa_id"] == j.sofifa_id].to_dict("records")
        if match:
            data = match[0]
            enriched_players.append({
                "long_name": j.long_name,
                "overall": j.overall,
                "player_positions": j.player_positions,
                "photo_url": data.get("player_face_url"),
                "club_logo_url": data.get("club_logo_url"),
                "nationality_flag_url": data.get("nation_flag_url"),
                "pace": j.pace,
                "shooting": j.shooting,
                "power_shot": j.power_shot,
                "defending": j.defending,
                "physical": j.physical,
                "goalkeeping_speed": j.goalkeeping_speed,
                "goalkeeping_diving": j.goalkeeping_diving,
                "goalkeeping_handling": j.goalkeeping_handling,
                "goalkeeping_kicking": j.goalkeeping_kicking,
                "goalkeeping_positioning": j.goalkeeping_positioning,
                "goalkeeping_reflexes": j.goalkeeping_reflexes,
                "age": j.age,
                "height_cm": j.height_cm,
                "club_name": j.club_name,
                "club_jersey_number": j.club_jersey_number,
                "position_category": j.position_category
            })

    return templates.TemplateResponse("player/list.html", {
        "request": request,
        "jugadores": enriched_players
    })
