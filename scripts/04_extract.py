import pandas as pd
import os

# Configuration des chemins
INPUT_PATH = "data/raw/tabular/listings.csv"
OUTPUT_PATH = "data/processed/filtered_elysee.csv"
QUARTIER = "Élysée"

# Sélection stratégique des colonnes (Hypothèses A et B)
COLS_TO_KEEP = [
    'id', 'listing_url', 'last_scraped',                      # Identifiants
    'host_id', 'host_response_time', 'host_response_rate',    # Hypothèse B (Social)
    'calculated_host_listings_count',                         # Hypothèse A (Industrie)
    'neighbourhood_cleansed', 'latitude', 'longitude',        # Localisation
    'property_type', 'room_type', 'accommodates',             # Caractéristiques
    'price', 'availability_365', 'number_of_reviews'          # Hypothèse A (Économie)
]

def run_extraction():
    if not os.path.exists(INPUT_PATH):
        print(f" Erreur : {INPUT_PATH} introuvable.")
        return

    print(f"Chargement et filtrage pour le quartier : {QUARTIER}...")
    
    # 1. Lecture
    df = pd.read_csv(INPUT_PATH)

    # 2. Filtrage géographique
    df_filtered = df[df['neighbourhood_cleansed'] == QUARTIER].copy()

    # 3. Sélection des colonnes
    df_final = df_filtered[COLS_TO_KEEP]

    # 4. Sauvegarde
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_final.to_csv(OUTPUT_PATH, index=False)
    
    print(f" Extraction terminée ! Fichier sauvegardé : {OUTPUT_PATH}")
    print(f"Volume extrait : {df_final.shape[0]} lignes et {df_final.shape[1]} colonnes.")

if __name__ == "__main__":
    run_extraction()