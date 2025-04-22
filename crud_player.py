from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database import Player
from player import Metricplayer

# Obtener todos los jugadores tipo Player
async def get_all_players(db: AsyncSession):
    result = await db.execute(select(Player))
    return result.scalars().all()

# Obtener un jugador tipo Player por ID
async def get_player(db: AsyncSession, sofifa_id: int):
    result = await db.execute(select(Player).where(Player.sofifa_id == sofifa_id))
    return result.scalar_one_or_none()
