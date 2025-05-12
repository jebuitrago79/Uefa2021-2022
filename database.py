import pandas as pd
import asyncio
from sqlmodel import SQLModel, Field, create_engine, Session
from models_sqlmodel import Jugador, Metricplayer

# Leer CSV
df = pd.read_csv("players_equipos_europeos_22.csv")

# Crear motor de base de datos (puedes cambiar a PostgreSQL si quieres luego)
DATABASE_URL = "sqlite:///uefa.db"  # Sin "async" porque usaremos Session síncrono aquí
engine = create_engine(DATABASE_URL, echo=False)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

def cargar_datos():
    with Session(engine) as session:
        for _, row in df.iterrows():
            jugador = Jugador(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=row["age"],
                nationality_name=row["nationality_name"],
                height_cm=row["height_cm"],
                club_name=row["club_name"],
                player_positions=row["player_positions"],
                club_jersey_number=row["club_jersey_number"]
            )

            metric = Metricplayer(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=row["age"],
                nationality_name=row["nationality_name"],
                height_cm=row["height_cm"],
                club_name=row["club_name"],
                player_positions=row["player_positions"],
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
