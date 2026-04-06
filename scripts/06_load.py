# 06_load.py
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

user     = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host     = os.getenv("DB_HOST", "localhost")
port     = os.getenv("DB_PORT", "5432")
dbname   = os.getenv("DB_NAME", "immovision_db")

chemin_csv = "data/processed/transformed_elysee.csv"
print(f"Lecture du fichier : {chemin_csv}")
df = pd.read_csv(chemin_csv)
print(f"{len(df)} lignes chargées depuis le CSV")

url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(url)
print(f"Connexion à PostgreSQL établie ({dbname})")

df.to_sql(
    name="elysee_listings_silver",
    con=engine,
    if_exists="replace",
    index=False
)

print(f"{len(df)} lignes chargées dans la table 'elysee_listings_silver'")
print("Load terminé avec succès !")