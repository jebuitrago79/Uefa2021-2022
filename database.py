import pandas as pd
import asyncio
from sqlalchemy import Column, Float, Integer, String, Boolean
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

class Player(Base):
    __tablename__ = "PLAYERS"
    sofifa_id = Column(Integer, primary_key=True, index=True)
    long_name = Column(String(70), nullable=False)
    age = Column(Integer, nullable=False)
    nationality_name = Column(String(40), nullable=False)
    height_cm = Column(Float, nullable=False)
    club_name = Column(String(40), nullable=False)
    player_positions = Column(String(40), nullable=False)
    club_jersey_number = Column(Float, nullable=False)
    overall = Column(Float, nullable=False)

    pace = Column(Float, nullable=True)
    shooting = Column(Float, nullable=True)
    defending = Column(Float, nullable=True)
    physical = Column(Float, nullable=True)
    power_shot = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)


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
                defending=row["defending"],
                physical=row["physic"],
                power_shot=row["power_shot_power"],
                club_jersey_number=row["club_jersey_number"]

            ))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(main())