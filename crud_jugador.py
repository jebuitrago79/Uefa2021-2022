from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import Jugadores
from jugador import Jugador


async def get_all_jugadores(db: AsyncSession):
    result = await db.execute(select(Jugadores))
    return result.scalars().all()


async def get_jugador(db: AsyncSession, sofifa_id: int):
    result = await db.execute(select(Jugadores).where(Jugadores.sofifa_id == sofifa_id))
    return result.scalar_one_or_none()

async def create_jugador(db: AsyncSession, jugador: Jugadores):
    new = Jugadores (**jugador.dict())
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return new

async def update_jugador(db: AsyncSession, sofifa_id: int, jugador: Jugador):
    db_jugador = await get_jugador(db, sofifa_id)
    if db_jugador is None:
        return None
    for key, value in jugador.dict().items():
        setattr(db_jugador, key, value)
    await db.commit()
    await db.refresh(db_jugador)
    return db_jugador