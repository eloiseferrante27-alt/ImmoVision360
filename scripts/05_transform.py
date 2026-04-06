import pandas as pd
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import time

# 1. Configuration
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

INPUT_CSV = "data/processed/filtered_elysee.csv"
OUTPUT_CSV = "data/processed/transformed_elysee.csv"
IMG_DIR = "data/raw/images/"
TXT_DIR = "data/raw/texts/"

def get_standardization_score(listing_id):
    """Analyse l'image via Gemini"""
    img_path = os.path.join(IMG_DIR, f"{listing_id}.jpg")
    if not os.path.exists(img_path):
        return "Image manquante"
    
    try:
        img = Image.open(img_path)
        prompt = "Analyse cette image d'appartement. Réponds UNIQUEMENT par un mot : 'Personnel' (si habité, vivant) ou 'Industrialisé' (si style hôtel, froid, standardisé)."
        response = model.generate_content([prompt, img])
        return response.text.strip()
    except Exception as e:
        return f"Erreur IA: {e}"

def clean_data(df):
    """Nettoyage de base"""
    # Exemple : Nettoyage du prix si c'est du texte ($1,200.00 -> 1200.0)
    if df['price'].dtype == 'object':
        df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
    
    # Imputation simple pour les notes manquantes
    df['host_response_rate'] = df['host_response_rate'].fillna("0%")
    return df

def run_transform():
    print(" Début de la transformation...")
    df = pd.read_csv(INPUT_CSV)
    df = clean_data(df)

    # ATTENTION : Pour tester, on ne prend que les 5 premières lignes
    # Supprime '.head(5)' une fois que tout fonctionne
    df_test = df.head(5).copy()

    print("Inférence IA en cours (Images)...")
    df_test['standardization_score'] = df_test['id'].apply(get_standardization_score)
    
    # Sauvegarde
    df_test.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Transformation terminée. Fichier prêt : {OUTPUT_CSV}")

if __name__ == "__main__":
    run_transform()