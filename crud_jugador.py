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
