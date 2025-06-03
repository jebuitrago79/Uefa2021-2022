import pandas as pd
from sqlmodel import SQLModel, create_engine, Session
from models_sqlmodel import Jugador, Metricplayer

# Si tu CSV original NO contiene las columnas “goals”, “assists”, etc.,
# en cargar_datos() simplemente NO intentes leerlas. Así quedarán en None.

DATABASE_URL = "sqlite:///uefa.db"
engine = create_engine(DATABASE_URL, echo=False)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

def cargar_datos():
    df = pd.read_csv("Jugadores_2021_22.csv")

    with Session(engine) as session:
        for _, row in df.iterrows():
            # Crea el Jugador sólo con los campos que SÍ vienen en el CSV:
            jugador = Jugador(
                sofifa_id = row["sofifa_id"],
                long_name = row["long_name"],
                age = row["age"],
                nationality_name = row["nationality_name"],
                height_cm = row["height_cm"],
                club_name = row.get("club_name"),
                player_positions = row.get("player_positions"),
                position_category = row.get("position_category"),
                club_jersey_number = row.get("club_jersey_number"),
                # NOTA: No incluyas aquí `goals=…` ni ninguno de los deseos; así quedan en None
                # goals=None, assists=None, etc.  (no hace falta ni ponerlos)
            )

            # Crea el Metricplayer de la misma forma:
            metric = Metricplayer(
                sofifa_id = row["sofifa_id"],
                long_name = row["long_name"],
                age = row["age"],
                nationality_name = row["nationality_name"],
                height_cm = row["height_cm"],
                club_name = row.get("club_name"),
                player_positions = row.get("player_positions"),
                position_category = row.get("position_category"),
                club_jersey_number = row.get("club_jersey_number"),
                overall = row.get("overall"),
                pace = row.get("pace"),
                shooting = row.get("shooting"),
                defending = row.get("defending"),
                physical = row.get("physic"),
                power_shot = row.get("power_shot_power"),
                goalkeeping_diving = row.get("goalkeeping_diving"),
                goalkeeping_handling = row.get("goalkeeping_handling"),
                goalkeeping_kicking = row.get("goalkeeping_kicking"),
                goalkeeping_positioning = row.get("goalkeeping_positioning"),
                goalkeeping_reflexes = row.get("goalkeeping_reflexes"),
                goalkeeping_speed = row.get("goalkeeping_speed"),
                is_active = True
            )

            session.add(jugador)
            session.add(metric)

        session.commit()

if __name__ == "__main__":
    # 1) Crea la BD / tablas (incluyendo columnas nuevas en Jugador)
    crear_tablas()
    # 2) Carga los datos del CSV (sólo con las columnas que realmente existen allí)
    cargar_datos()

