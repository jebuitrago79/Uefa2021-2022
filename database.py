import pandas as pd
import asyncio
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

df = pd.read_csv("players_equipos_europeos_22.csv")


class Base(DeclarativeBase):
    pass

class Jugadores(Base):
    __tablename__ = "JUGADORES"
    sofifa_id: Mapped[int] = mapped_column(primary_key=True)
    long_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    player_positions: Mapped[str] = mapped_column(String(50), nullable=True)
    nationality_name: Mapped[str] = mapped_column(String(60))
    height_cm: Mapped[float] = mapped_column(Float)
    club_name: Mapped[str] = mapped_column(String(100))
    club_jersey_number: Mapped[float] = mapped_column(Float)

# Modelo Player
class Player(Base):
    __tablename__ = "PLAYERS"
    sofifa_id: Mapped[int] = mapped_column(primary_key=True)
    long_name: Mapped[str] = mapped_column(String(100))
    player_positions: Mapped[str] = mapped_column(String(50), nullable=True)
    overall: Mapped[int] = mapped_column(Integer)
    age: Mapped[int] = mapped_column(Integer)
    height_cm: Mapped[float] = mapped_column(Float)
    club_name: Mapped[str] = mapped_column(String(100))
    nationality_name: Mapped[str] = mapped_column(String(60))
    pace: Mapped[float] = mapped_column(Float, nullable=True)
    shooting: Mapped[float] = mapped_column(Float, nullable=True)
    passing: Mapped[float] = mapped_column(Float, nullable=True)
    defending: Mapped[float] = mapped_column(Float, nullable=True)
    physic: Mapped[float] = mapped_column(Float, nullable=True)
    power_shot_power: Mapped[float] = mapped_column(Float, nullable=True)
    club_jersey_number: Mapped[float] = mapped_column(Float, nullable=True)

DATABASE_URL = "sqlite+aiosqlite:///./uefa.db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def main():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        for _, row in df.iterrows():
            session.add(Jugadores(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=row["age"],
                player_positions=row["player_positions"],
                nationality_name=row["nationality_name"],
                height_cm=row["height_cm"],
                club_name=row["club_name"],
                club_jersey_number=row["club_jersey_number"]
            ))

            session.add(Player(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                player_positions=row["player_positions"],
                overall=row["overall"],
                age=row["age"],
                height_cm=row["height_cm"],
                club_name=row["club_name"],
                nationality_name=row["nationality_name"],
                pace=row["pace"],
                shooting=row["shooting"],
                passing=row["passing"],
                defending=row["defending"],
                physic=row["physic"],
                power_shot_power=row["power_shot_power"],
                club_jersey_number=row["club_jersey_number"]
            ))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())