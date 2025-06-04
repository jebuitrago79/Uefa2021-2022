# routers/players.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi.responses import JSONResponse
from typing import List
from models_sqlmodel import Metricplayer, MetricplayerPatchBody
from database import get_session
from crud_player import (
    get_all_players, get_player, create_player, update_player,
    delete_player, get_players_by_overall, json_safe, patch_metricplayer
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from supabase import get_player_images

templates = Jinja2Templates(directory="templates")

from fastapi import APIRouter
router = APIRouter(tags=["FIFA Players"])


from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_session
from crud_player import get_all_players
from sqlmodel import select
from models_sqlmodel import Metricplayer

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["FIFA Players"])

@router.get("/players", response_class=HTMLResponse)
async def player_list_web(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = 25
):
    offset = (page - 1) * limit

    result = await session.execute(select(Metricplayer))
    total_jugadores = len(result.scalars().all())

    paginated_result = await session.execute(
        select(Metricplayer).offset(offset).limit(limit)
    )
    jugadores_db = paginated_result.scalars().all()

    jugadores = []
    for jugador in jugadores_db:
        imagenes = await get_player_images(jugador.sofifa_id)
        jugador_dict = jugador.model_dump()
        jugador_dict["photo_url"] = imagenes.get("player_face_url")
        jugador_dict["club_logo_url"] = imagenes.get("club_logo_url")
        jugador_dict["nationality_flag_url"] = imagenes.get("nation_flag_url")
        jugadores.append(jugador_dict)

    total_pages = (total_jugadores + limit - 1) // limit

    return templates.TemplateResponse("player/list.html", {
        "request": request,
        "jugadores": jugadores,
        "page": page,
        "total_pages": total_pages
    })




