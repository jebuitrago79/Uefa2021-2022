from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import Jugadores
from jugador import Jugador
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, delete

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

async def update_jugador(db_session: AsyncSession, sofifa_id: int, data: dict):
    data.pop("sofifa_id", None)

    query = (
        update(Jugadores)
        .where(Jugadores.sofifa_id == sofifa_id)
        .values(**data)
    )
    result = await db_session.execute(query)
    await db_session.commit()
    return result.rowcount > 0



async def delete_jugador(db_session: AsyncSession, sofifa_id: int):
    result = await db_session.execute(
        delete(Jugadores).where(Jugadores.sofifa_id == sofifa_id)
    )
    await db_session.commit()
    return result.rowcount > 0

async def export_jugadores_to_csv(db: AsyncSession, filepath: str = "jugadores.csv"):
    result = await db.execute(select(Jugadores))
    jugadores = result.scalars().all()

    data = [
        {
            "sofifa_id": j.sofifa_id,
            "long_name": j.long_name,
            "age": j.age,
            "nationality_name": j.nationality_name,
            "height_cm": j.height_cm,
            "club_name": j.club_name,
            "player_positions": j.player_positions,
            "club_jersey_number": j.club_jersey_number
        }
        for j in jugadores
    ]

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    return filepath

async def get_jugadores_by_pais(db: AsyncSession, pais: str):
    result = await db.execute(
        select(Jugadores).where(Jugadores.nationality_name.ilike(f"%{pais}%"))
    )
    return result.scalars().all()