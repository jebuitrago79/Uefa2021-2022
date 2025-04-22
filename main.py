from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud_jugador import *
from database import *
from jugador import Jugador
from typing import List
from crud_player import *
from player import Metricplayer

app = FastAPI()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/jugadores", response_model=List[Jugador])
async def read_jugadores(db: AsyncSession = Depends(get_db)):
    return await get_all_jugadores(db)

@app.get("/jugadores/{sofifa_id}", response_model=Jugador)
async def read_jugador(sofifa_id: int, db: AsyncSession = Depends(get_db)):
    jugador = await get_jugador(db, sofifa_id)
    if jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@app.post("/jugadores", response_model=Jugador)
async def create_jugador1(jugador: Jugador, db: AsyncSession = Depends(get_db)):
    return await create_jugador(db,jugador)



@app.put("/jugadores/{sofifa_id}", response_model=Jugador)
async def update_jugador1(
    sofifa_id: int,
    jugador_update: Jugador,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_jugador(
        db, sofifa_id, jugador_update.dict(exclude_unset=True)
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Jugador no modificado")

    jugador_actualizado = await get_jugador(db, sofifa_id)
    return jugador_actualizado

@app.delete("/jugadores/{sofifa_id}", response_model=Jugador)
async def delete_jugador_endpoint(sofifa_id: int, db: AsyncSession = Depends(get_db)):
    jugador = await get_jugador(db, sofifa_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    eliminado = await delete_jugador(db, sofifa_id)
    if not eliminado:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el jugador")

    return jugador


@app.get("/players", response_model=List[Metricplayer])
async def read_players(db: AsyncSession = Depends(get_db)):
    return await get_all_players(db)

@app.get("/players/{sofifa_id}", response_model=Metricplayer)
async def read_player(sofifa_id: int, db: AsyncSession = Depends(get_db)):
    player = await get_player(db, sofifa_id)
    if not player:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return player

@app.post("/players", response_model=Metricplayer)
async def create_new_player(player: Metricplayer, db: AsyncSession = Depends(get_db)):
    return await create_player(db, player)

@app.put("/players/{sofifa_id}", response_model=Metricplayer)
async def update_existing_player(
    sofifa_id: int,
    player_update: Metricplayer,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_player(db, sofifa_id, player_update.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Jugador no actualiazado")
    return await get_player(db, sofifa_id)

@app.delete("/players/{sofifa_id}", response_model=Metricplayer)
async def delete_player_detailed(sofifa_id: int, db: AsyncSession = Depends(get_db)):
    player = await get_player(db, sofifa_id)
    if not player:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    success = await delete_player(db, sofifa_id)
    if not success:
        raise HTTPException(status_code=400, detail="No se pudo eliminar el jugador")

    return player