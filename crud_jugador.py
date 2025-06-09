from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models_sqlmodel import Jugador, PlayerCategory


async def get_all_jugadores(session: AsyncSession) -> List[Jugador]:
    result = await session.execute(select(Jugador))
    return result.scalars().all()


async def get_jugador(session: AsyncSession, sofifa_id: int) -> Optional[Jugador]:
    return await session.get(Jugador, sofifa_id)


async def create_jugador(session: AsyncSession, jugador: Jugador) -> Jugador:
    session.add(jugador)
    await session.commit()
    await session.refresh(jugador)
    return jugador


async def patch_jugador(session: AsyncSession, sofifa_id: int, data: dict) -> Optional[Jugador]:
    jugador = await session.get(Jugador, sofifa_id)
    if not jugador:
        return None

    for key, value in data.items():
        if key == "position_category" and isinstance(value, str):
            value = PlayerCategory(value)
        setattr(jugador, key, value)

    session.add(jugador)
    await session.commit()
    await session.refresh(jugador)
    return jugador


async def delete_jugador(session: AsyncSession, sofifa_id: int) -> bool:
    jugador = await session.get(Jugador, sofifa_id)
    if not jugador:
        return False
    await session.delete(jugador)
    await session.commit()
    return True

async def get_jugadores_by_pais(session: AsyncSession, pais: str) -> List[Jugador]:
    result = await session.execute(
        select(Jugador).where(Jugador.nationality_name.ilike(f"%{pais}%"))
    )
    return result.scalars().all()

