from fastapi import FastAPI, Depends, HTTPException, Path, Body, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from models_sqlmodel import Jugador, JugadorPatchBody, Metricplayer, MetricplayerPatchBody
from database import get_session
from crud_jugador import (
    get_all_jugadores,
    get_jugador,
    get_jugadores_by_pais,
    create_jugador,
    patch_jugador,
    delete_jugador
)
from models_sqlmodel import Metricplayer
from crud_player import (
    get_all_players,
    get_player,
    create_player,
    update_player,
    delete_player,
    get_players_by_overall,
    json_safe,
    patch_metricplayer
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API UEFA 2021-2022."}


@app.get("/jugadores", response_model=List[Jugador])
async def read_jugadores(session: AsyncSession = Depends(get_session)):
    return await get_all_jugadores(session)


@app.get("/jugadores/{sofifa_id}", response_model=Jugador)
async def read_jugador_by_id(sofifa_id: int, session: AsyncSession = Depends(get_session)):
    jugador = await get_jugador(session, sofifa_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@app.get("/jugadores/pais/{pais}", response_model=List[Jugador])
async def jugadores_por_pais(pais: str, session: AsyncSession = Depends(get_session)):
    return await get_jugadores_by_pais(session, pais)


@app.post("/jugadores", response_model=Jugador)
async def create_jugador_endpoint(jugador: Jugador, session: AsyncSession = Depends(get_session)):
    return await create_jugador(session, jugador)


from models_sqlmodel import JugadorPatchBody

@app.patch("/jugadores/{sofifa_id}", response_model=Jugador)
async def patch_jugador_endpoint(
    sofifa_id: int,
    payload: JugadorPatchBody,
    session: AsyncSession = Depends(get_session)
):
    jugador = await patch_jugador(session, sofifa_id, payload.dict(exclude_unset=True))
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@app.delete("/jugadores/{sofifa_id}")
async def delete_jugador_endpoint(sofifa_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_jugador(session, sofifa_id)
    if not success:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": "Jugador eliminado correctamente"}


@app.get("/fifa_players", response_model=List[Metricplayer])
async def read_players(session: AsyncSession = Depends(get_session)):
    players = await get_all_players(session)
    return json_safe(players)



@app.get("/fifa_players/{sofifa_id}", response_model=Metricplayer)
async def read_player_by_id(sofifa_id: int, session: AsyncSession = Depends(get_session)):
    player = await get_player(session, sofifa_id)
    if not player:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return json_safe(player)



@app.get("/fifa_players/overall/{min_overall}")
async def read_players_by_overall(
    min_overall: float = Path(..., ge=0, description="Minimum overall rating (must be 0 or higher)"),
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Metricplayer).where(Metricplayer.overall >= min_overall)
    )
    jugadores = result.scalars().all()
    return JSONResponse(content=json_safe(jugadores))



@app.post("/fifa_players", response_model=Metricplayer)
async def create_player_endpoint(player: Metricplayer, session: AsyncSession = Depends(get_session)):
    return await create_player(session, player)


@app.patch("/metricplayers/{sofifa_id}", response_model=Metricplayer)
async def patch_metricplayer_endpoint(
    sofifa_id: int,
    payload: MetricplayerPatchBody,
    session: AsyncSession = Depends(get_session)
):
    jugador = await patch_metricplayer(session, sofifa_id, payload.dict(exclude_unset=True))
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador


@app.delete("/fifa_players/{sofifa_id}")
async def delete_player_endpoint(sofifa_id: int, session: AsyncSession = Depends(get_session)):
    success = await delete_player(session, sofifa_id)
    if not success:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return {"message": "Jugador marcado como inactivo"}