from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "data" / "processed" / "transformed_elysee.csv"


def run_load() -> None:
    load_dotenv()

    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "immovision_db")

    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Fichier introuvable: {INPUT_CSV}")

    if not user:
        raise EnvironmentError("DB_USER doit être défini dans l'environnement.")

    df = pd.read_csv(INPUT_CSV)
    if df.empty:
        raise ValueError("Le CSV transformé est vide, chargement annulé.")

    if password:
        database_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    else:
        database_url = f"postgresql://{user}@{host}:{port}/{dbname}"

    engine = create_engine(database_url)
    df.to_sql(
        name="elysee_listings_silver",
        con=engine,
        if_exists="replace",
        index=False,
    )

    print(f"Chargement terminé: {len(df)} lignes vers elysee_listings_silver")


if __name__ == "__main__":
    run_load()
