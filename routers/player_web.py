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
from Enum import PlayerCategory
from typing import Optional
from supabase import insertar_imagen_supabase

templates = Jinja2Templates(directory="templates")

from fastapi import APIRouter
from supabase import actualizar_imagen_supabase
from fastapi import APIRouter, Request, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_session
from crud_player import get_all_players
from sqlmodel import select
from models_sqlmodel import Metricplayer
from fastapi import Form, Request, status
from fastapi.responses import RedirectResponse
from crud_player import create_player
from starlette.status import HTTP_303_SEE_OTHER

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


@router.get("/players/create", response_class=HTMLResponse)
async def create_player_form(request: Request):
    return templates.TemplateResponse("player/create.html", {
        "request": request
    })


@router.post("/players/create")
async def post_create_form(
        request: Request,
        sofifa_id: int = Form(...),
        long_name: str = Form(...),
        age: int = Form(...),
        nationality_name: str = Form(...),
        height_cm: float = Form(...),
        club_name: str = Form(""),
        player_positions: str = Form(""),
        club_jersey_number: Optional[float] = Form(None),
        overall: float = Form(0),
        pace: float = Form(0),
        shooting: float = Form(0),
        defending: float = Form(0),
        physical: float = Form(0),
        power_shot: float = Form(0),
        position_category: PlayerCategory = Form(...),
        goalkeeping_diving: float = Form(0),
        goalkeeping_handling: float = Form(0),
        goalkeeping_kicking: float = Form(0),
        goalkeeping_positioning: float = Form(0),
        goalkeeping_reflexes: float = Form(0),
        goalkeeping_speed: float = Form(0),
        is_active: bool = Form(True),
        photo_url: str = Form(...),
        nationality_flag_url: str = Form(...),
        club_logo_url: str = Form(...),
        session: AsyncSession = Depends(get_session)
):
    new_player = Metricplayer(
        sofifa_id=sofifa_id,
        long_name=long_name,
        age=age,
        nationality_name=nationality_name,
        height_cm=height_cm,
        club_name=club_name,
        player_positions=player_positions,
        club_jersey_number=club_jersey_number,
        overall=overall,
        pace=pace,
        shooting=shooting,
        defending=defending,
        physical=physical,
        power_shot=power_shot,
        position_category=position_category,
        goalkeeping_diving=goalkeeping_diving,
        goalkeeping_handling=goalkeeping_handling,
        goalkeeping_kicking=goalkeeping_kicking,
        goalkeeping_positioning=goalkeeping_positioning,
        goalkeeping_reflexes=goalkeeping_reflexes,
        goalkeeping_speed=goalkeeping_speed,
        is_active=is_active,
        photo_url=photo_url,
        nationality_flag_url=nationality_flag_url,
        club_logo_url=club_logo_url
    )

    await create_player(session, new_player)

    await insertar_imagen_supabase(
        sofifa_id=sofifa_id,
        photo_url=photo_url,
        club_logo_url=club_logo_url,
        nationality_flag_url=nationality_flag_url
    )

    return RedirectResponse(url="/players", status_code=HTTP_303_SEE_OTHER)


@router.post("/players/delete/{player_id}")
async def delete_player(player_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Metricplayer).where(Metricplayer.id == player_id)
    result = await session.execute(statement)
    player = result.scalar_one_or_none()

    if player:
        player.is_active = not player.is_active
        session.add(player)
        await session.commit()
        await session.refresh(player)

    return RedirectResponse(url="/players", status_code=303)


@router.get("/players/edit/{player_id}", response_class=HTMLResponse)
async def edit_player_form(player_id: int, request: Request, session: AsyncSession = Depends(get_session)):
    jugador = await session.get(Metricplayer, player_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    return templates.TemplateResponse("player/edit.html", {
        "request": request,
        "jugador": jugador
    })


@router.post("/players/edit/{player_id}")
async def update_player(
    player_id: int,
    long_name: str = Form(...),
    age: int = Form(...),
    nationality_name: str = Form(...),
    nationality_flag_url: str = Form(""),
    height_cm: float = Form(...),
    club_name: str = Form(...),
    club_logo_url: str = Form(""),
    player_positions: str = Form(...),
    club_jersey_number: float = Form(...),
    position_category: PlayerCategory = Form(...),
    session: AsyncSession = Depends(get_session),
):
    jugador = await session.get(Metricplayer, player_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    jugador.long_name = long_name
    jugador.age = age
    jugador.nationality_name = nationality_name
    jugador.nationality_flag_url = nationality_flag_url
    jugador.height_cm = height_cm
    jugador.club_name = club_name
    jugador.club_logo_url = club_logo_url
    jugador.player_positions = player_positions
    jugador.club_jersey_number = club_jersey_number
    jugador.position_category = position_category

    await session.commit()

    try:
        await actualizar_imagen_supabase(jugador.sofifa_id, nationality_flag_url, club_logo_url)
    except Exception as e:
        print(f"⚠️ Error actualizando en Supabase: {e}")

    return RedirectResponse(url="/players", status_code=303)

