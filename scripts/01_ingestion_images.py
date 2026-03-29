import pandas as pd
import requests
import os
import time
import random
from PIL import Image
from io import BytesIO

# --- CONFIGURATION ---
CSV_PATH = "../data/raw/tabular/listings.csv"
OUTPUT_DIR = "../data/raw/images/"
TARGET_NEIGHBOURHOOD = "Élysée"
IMAGE_SIZE = (320, 320)
HEADERS = {'User-Agent': 'ImmoVision360/1.0 (Academic Project; Contact: student@univ.fr)'}

def ingest_images():
    # 1. Chargement et filtrage
    if not os.path.exists(CSV_PATH):
        print(f"Erreur : {CSV_PATH} introuvable.")
        return

    df = pd.read_csv(CSV_PATH)
    # Filtrage sur le quartier spécifique (selon la colonne officielle Airbnb)
    df_filtered = df[df['neighbourhood_cleansed'] == TARGET_NEIGHBOURHOOD]
    
    print(f" Début de l'ingestion pour {len(df_filtered)} annonces à {TARGET_NEIGHBOURHOOD}...")

    # 2. Boucle de traitement
    for index, row in df_filtered.iterrows():
        listing_id = str(row['id'])
        img_url = row['picture_url']
        filename = f"{listing_id}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # PILIER : Idempotence (On ne télécharge pas si déjà présent)
        if os.path.exists(filepath):
            continue

        # GESTION DES EXCEPTIONS : Try/Except pour la robustesse
        try:
            # 3. Requête réseau (Courtoisie : Timeout inclus)
            response = requests.get(img_url, headers=HEADERS, timeout=15)
            
            if response.status_code == 200:
                # 4. Traitement Image (Redimensionnement 320x320)
                img = Image.open(BytesIO(response.content))
                img = img.convert('RGB') # Sécurité pour les formats PNG/WebP
                img = img.resize(IMAGE_SIZE)
                
                # 5. Sauvegarde
                img.save(filepath, "JPEG")
                print(f"Image {filename} enregistrée.")
                
                # RÈGLE D'OR : Rate Limiting (Pause aléatoire)
                time.sleep(random.uniform(0.5, 1.2))
            else:
                print(f"Lien mort (Code {response.status_code}) pour l'ID {listing_id}")

        except Exception as e:
            print(f" Erreur critique pour l'ID {listing_id} : {e}")

    print("\nTravail terminé. La zone Bronze (Images) est prête.")

if __name__ == "__main__":
    ingest_images()