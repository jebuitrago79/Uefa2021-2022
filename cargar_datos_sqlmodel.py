import pandas as pd
from sqlmodel import SQLModel, create_engine, Session
from models_sqlmodel import Jugador, Metricplayer


DATABASE_URL = "sqlite:///uefa.db"
engine = create_engine(DATABASE_URL, echo=False)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

def cargar_datos():
    df = pd.read_csv("Jugadores_2021_22.csv")

    with Session(engine) as session:
        for _, row in df.iterrows():

            jugador = Jugador(
                sofifa_id=row["sofifa_id"],
                long_name=row["long_name"],
                age=int(row["age"]),
                nationality_name=row["nationality_name"],
                height_cm=int(row["height_cm"]),
                club_name=row.get("club_name"),
                player_positions=row.get("player_positions"),
                position_category=row.get("position_category"),
                club_jersey_number=row.get("club_jersey_number"),
                goals=int(row.get("goals", 0)),
                assists=int(row.get("assists", 0)),
                yellow_cards=int(row.get("yellow_cards", 0)),
                red_cards=int(row.get("red_cards", 0)),
                saved=int(row.get("saved", 0)),
                conceded=int(row.get("conceded", 0)),
                games=int(row.get("games", 0)),
                saves=int(row.get("saves", 0)),
                goals_conceded=int(row.get("goals_conceded", 0)),
                clean_Sheets=int(row.get("clean_Sheets", 0)),
                tackles=int(row.get("tackles", 0)),
                interceptions=int(row.get("interceptions", 0)),
                fouls=int(row.get("fouls", 0)),
                photo_url=row.get("photo_url"),
                nationality_flag_url=row.get("nation_logo_url"),
                club_logo_url=row.get("club_logo_url"),
                is_active=True
            )

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
                photo_url=row.get("photo_url"),
                nationality_flag_url=row.get("nation_logo_url"),
                club_logo_url=row.get("club_logo_url"),
                is_active = True
            )

            session.add(jugador)
            session.add(metric)

        session.commit()

if __name__ == "__main__":

    crear_tablas()

    cargar_datos()

