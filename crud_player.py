from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database import Player
from player import Metricplayer
import pandas as pd


async def get_all_players(db: AsyncSession):
    result = await db.execute(
        select(Player).where(Player.is_active == True)
    )
    return result.scalars().all()


async def get_player(db: AsyncSession, sofifa_id: int):
    result = await db.execute(select(Player).where(Player.sofifa_id == sofifa_id))
    return result.scalar_one_or_none()


async def create_player(db: AsyncSession, player: Metricplayer):
    new_player = Player(**player.dict())
    db.add(new_player)
    await db.commit()
    await db.refresh(new_player)
    return new_player


async def update_player(db_session: AsyncSession, sofifa_id: int, data: dict):
    data.pop("sofifa_id", None)
    query = (
        update(Player)
        .where(Player.sofifa_id == sofifa_id)
        .values(**data)
    )
    result = await db_session.execute(query)
    await db_session.commit()
    return result.rowcount > 0

async def delete_player(db: AsyncSession, sofifa_id: int):
    query = (
        update(Player)
        .where(Player.sofifa_id == sofifa_id)
        .values(is_active=False)
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0

async def export_players_to_csv(db: AsyncSession, filepath: str = "players.csv"):
    result = await db.execute(select(Player))
    players = result.scalars().all()

    data = [
        {
            "sofifa_id": p.sofifa_id,
            "long_name": p.long_name,
            "age": p.age,
            "nationality_name": p.nationality_name,
            "height_cm": p.height_cm,
            "club_name": p.club_name,
            "player_positions": p.player_positions,
            "club_jersey_number": p.club_jersey_number,
            "overall": p.overall,
            "pace": p.pace,
            "shooting": p.shooting,
            "defending": p.defending,
            "physical": p.physical,
            "power_shot": p.power_shot
        }
        for p in players
    ]

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)


async def get_players_by_overall(db: AsyncSession, min_overall: float):
    result = await db.execute(
        select(Player).where(Player.overall >= min_overall)
    )
    return result.scalars().all()