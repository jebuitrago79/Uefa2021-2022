import pandas as pd
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from models_sqlmodel import Jugador, Metricplayer

df = pd.read_csv("Player_Equipos_Europeos2021_22.csv")


DATABASE_URL = "sqlite+aiosqlite:///./uefa.db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


sync_engine = create_engine("sqlite:///uefa.db", echo=False)

def crear_tablas():
    SQLModel.metadata.create_all(sync_engine)

def cargar_datos():
    with Session(sync_engine) as session:
        for _, row in df.iterrows():
            jugador = Jugador(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=row["age"],
                nationality_name=row["nationality_name"],
                height_cm=row["height_cm"],
                club_name=row["club_name"],
                position_category=PlayerCategory(row["position_category"]),
                club_jersey_number=row["club_jersey_number"]
            )

            metric = Metricplayer(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=row["age"],
                nationality_name=row["nationality_name"],
                height_cm=row["height_cm"],
                club_name=row["club_name"],
                position_category=PlayerCategory(row["position_category"]),
                club_jersey_number=row["club_jersey_number"],
                overall=row["overall"],
                pace=row.get("pace"),
                shooting=row.get("shooting"),
                defending=row.get("defending"),
                physical=row.get("physic"),
                power_shot=row.get("power_shot_power"),
                is_active=True
            )

            session.add(jugador)
            session.add(metric)

        session.commit()

if __name__ == "__main__":
    crear_tablas()
    cargar_datos()
