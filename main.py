from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud_jugador import *
from database import AsyncSessionLocal
from jugador import Jugador
from typing import List

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
async def delete_jugador1(sofifa_id: int, db: AsyncSession = Depends(get_db)):
    jugador = await get_jugador(db, sofifa_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")

    eliminado = await delete_jugador(db, sofifa_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Jugador no eliminado")

    return jugador