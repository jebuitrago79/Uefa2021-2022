from fastapi import APIRouter, Request, Depends, Query, status, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models_sqlmodel import Jugador, Metricplayer
from supabase import  get_player_images
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
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


@router.get("/jugadores/{sofifa_id}/stats-form", response_class=HTMLResponse)
async def mostrar_formulario_stats(
    sofifa_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    jugador = await session.get(Jugador, sofifa_id)
    if not jugador:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("Jugadores/stats_form.html", {
        "request": request,
        "jugador": jugador
    })


@router.post("/jugadores/{sofifa_id}/stats-form")
async def guardar_stats_jugador(
    sofifa_id: int,
    request: Request,
    goals: int = Form(...),
    assists: int = Form(...),
    yellow_cards: int = Form(...),
    red_cards: int = Form(...),
    saved: int = Form(...),
    games: int = Form(...),
    saves: int = Form(...),
    goals_conceded: int = Form(...),
    clean_Sheets: int = Form(...),
    tackles: int = Form(...),
    interceptions: int = Form(...),
    fouls: int = Form(...),
    session: AsyncSession = Depends(get_session)
):
    jugador = await session.get(Jugador, sofifa_id)
    if not jugador:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    # Guardar campos en el modelo
    jugador.goals = goals
    jugador.assists = assists
    jugador.yellow_cards = yellow_cards
    jugador.red_cards = red_cards
    jugador.saved = saved
    jugador.games = games
    jugador.saves = saves
    jugador.goals_conceded = goals_conceded
    jugador.clean_Sheets = clean_Sheets
    jugador.tackles = tackles
    jugador.interceptions = interceptions
    jugador.fouls = fouls

    session.add(jugador)
    await session.commit()

    # Redirige a la vista de comparación
    return RedirectResponse(f"/jugadores/{sofifa_id}/comparar", status_code=303)


@router.get("/jugadores/{sofifa_id}/comparar", response_class=HTMLResponse)
async def comparar_stats(
    request: Request,
    sofifa_id: int,
    session: AsyncSession = Depends(get_session)
):
    jugador = await session.get(Jugador, sofifa_id)
    fifa = await session.get(Metricplayer, sofifa_id)

    if not jugador or not fifa:
        raise HTTPException(status_code=404, detail="Jugador o carta FIFA no encontrado")

    # 🧠 Cálculo del overall basado en estadísticas reales
    if jugador.games and jugador.games > 0:
        goles_por_partido = jugador.goals / jugador.games if jugador.goals is not None else 0
        asistencias_por_partido = jugador.assists / jugador.games if jugador.assists is not None else 0
        tackles_por_partido = jugador.tackles / jugador.games if jugador.tackles is not None else 0
        intercepciones_por_partido = jugador.interceptions / jugador.games if jugador.interceptions is not None else 0
        fouls_por_partido = jugador.fouls / jugador.games if jugador.fouls is not None else 0

        overall = (
            (goles_por_partido * 25) +
            (asistencias_por_partido * 20) +
            (tackles_por_partido * 5) +
            (intercepciones_por_partido * 5) +
            ((1 - fouls_por_partido) * 5) +  # menos faltas = mejor
            39  # base para ajustarse al estilo FIFA
        )
        overall_estimado = min(max(round(overall), 0), 99)
    else:
        overall_estimado = 0

    imagen = await get_player_images(jugador.sofifa_id)

    return templates.TemplateResponse("Jugadores/comparacion.html", {
        "request": request,
        "jugador": jugador,
        "fifa": fifa,
        "imagen": imagen,
        "overall_estimado": overall_estimado
    })
