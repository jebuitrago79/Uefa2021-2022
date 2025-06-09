from fastapi import APIRouter, Request, Depends, Query, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models_sqlmodel import Jugador
from supabase import  get_player_images
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/jugadores", response_class=HTMLResponse)
async def mostrar_jugadores(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, ge=1),
    limit: int = 25
):
    offset = (page - 1) * limit

    total_result = await session.execute(select(Jugador))
    total_jugadores = len(total_result.scalars().all())

    paginated_result = await session.execute(
        select(Jugador).offset(offset).limit(limit)
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

    return templates.TemplateResponse("Jugadores/list.html", {
        "request": request,
        "jugadores": jugadores,
        "page": page,
        "total_pages": total_pages
    })