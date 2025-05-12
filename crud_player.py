from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models_sqlmodel import Metricplayer, PlayerCategory


async def get_all_players(session: AsyncSession) -> List[Metricplayer]:
    result = await session.execute(
        select(Metricplayer).where(Metricplayer.is_active == True)
    )
    return result.scalars().all()


async def get_player(session: AsyncSession, sofifa_id: int) -> Optional[Metricplayer]:
    return await session.get(Metricplayer, sofifa_id)


async def create_player(session: AsyncSession, player: Metricplayer) -> Metricplayer:
    session.add(player)
    await session.commit()
    await session.refresh(player)
    return player



async def patch_metricplayer(session: AsyncSession, sofifa_id: int, data: dict) -> Optional[Metricplayer]:
    jugador = await session.get(Metricplayer, sofifa_id)
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


async def delete_player(session: AsyncSession, sofifa_id: int) -> bool:
    player = await session.get(Metricplayer, sofifa_id)
    if not player:
        return False
    player.is_active = False
    await session.commit()
    return True


async def get_players_by_overall(session: AsyncSession, min_overall: float) -> List[Metricplayer]:
    result = await session.execute(
        select(Metricplayer).where(Metricplayer.overall >= min_overall, Metricplayer.is_active == True)
    )
    return result.scalars().all()
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models_sqlmodel import Metricplayer


async def get_all_players(session: AsyncSession) -> List[Metricplayer]:
    result = await session.execute(
        select(Metricplayer).where(Metricplayer.is_active == True)
    )
    return result.scalars().all()


async def get_player(session: AsyncSession, sofifa_id: int) -> Optional[Metricplayer]:
    return await session.get(Metricplayer, sofifa_id)


async def create_player(session: AsyncSession, player: Metricplayer) -> Metricplayer:
    session.add(player)
    await session.commit()
    await session.refresh(player)
    return player


async def update_player(session: AsyncSession, sofifa_id: int, data: dict) -> Optional[Metricplayer]:
    player = await session.get(Metricplayer, sofifa_id)
    if not player:
        return None
    for key, value in data.items():
        setattr(player, key, value)
    session.add(player)
    await session.commit()
    await session.refresh(player)
    return player


async def delete_player(session: AsyncSession, sofifa_id: int) -> bool:
    player = await session.get(Metricplayer, sofifa_id)
    if not player:
        return False
    player.is_active = False
    await session.commit()
    return True

