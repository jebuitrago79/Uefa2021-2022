import os
import pandas as pd
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from models_sqlmodel import Jugador, Metricplayer, PlayerCategory

load_dotenv()

# Datos de conexión a Clever Cloud
DB_USER = os.getenv("POSTGRESQL_ADDON_USER")
DB_PASS = os.getenv("POSTGRESQL_ADDON_PASSWORD")
DB_HOST = os.getenv("POSTGRESQL_ADDON_HOST")
DB_PORT = os.getenv("POSTGRESQL_ADDON_PORT")
DB_NAME = os.getenv("POSTGRESQL_ADDON_DB")

ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SYNC_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

df = pd.read_csv("Jugadores_2021_22.csv")


df.replace({pd.NA: None, "NaN": None}, inplace=True)

def safe_float(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def safe_category(val):
    try:
        return PlayerCategory(val)
    except (ValueError, TypeError):
        return None

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

def crear_tablas():
    SQLModel.metadata.create_all(sync_engine)

def cargar_datos():
    with Session(sync_engine) as session:
        for _, row in df.iterrows():
            jugador = Jugador(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=int(row["age"]),
                nationality_name=row["nationality_name"],
                height_cm=int(row["height_cm"]),
                club_name=row.get("club_name"),
                position_category=safe_category(row.get("position_category")),
                club_jersey_number=safe_float(row.get("club_jersey_number")),
            )

            metric = Metricplayer(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=int(row["age"]),
                nationality_name=row["nationality_name"],
                height_cm=int(row["height_cm"]),
                club_name=row.get("club_name"),
                player_positions=row.get("player_positions") or "Unknown",
                position_category=safe_category(row.get("position_category")),
                club_jersey_number=safe_float(row.get("club_jersey_number")),
                overall=safe_float(row.get("overall")),
                pace=safe_float(row.get("pace")),
                shooting=safe_float(row.get("shooting")),
                defending=safe_float(row.get("defending")),
                physical=safe_float(row.get("physic")),
                power_shot=safe_float(row.get("power_shot_power")),
                goalkeeping_diving=safe_float(row.get("goalkeeping_diving")),
                goalkeeping_handling=safe_float(row.get("goalkeeping_handling")),
                goalkeeping_kicking=safe_float(row.get("goalkeeping_kicking")),
                goalkeeping_positioning=safe_float(row.get("goalkeeping_positioning")),
                goalkeeping_reflexes=safe_float(row.get("goalkeeping_reflexes")),
                goalkeeping_speed=safe_float(row.get("goalkeeping_speed")),
                photo_url=row.get("photo_url"),
                nationality_flag_url=row.get("nation_logo_url"),
                club_logo_url=row.get("club_logo_url"),
                is_active=True
            )

            session.add(jugador)
            session.add(metric)

        session.commit()

def verificar_conexion():
    with Session(sync_engine) as session:
        result = session.exec(select(Jugador)).all()
        print(f"✅ Total de jugadores en la base: {len(result)}")

if __name__ == "__main__":
    try:
        crear_tablas()
        print("✅ Tablas creadas correctamente")
        cargar_datos()
        print("✅ Datos cargados correctamente")
        verificar_conexion()
    except Exception as e:
        print("❌ Error durante la ejecución:", e)

