import pandas as pd
import os
import re

# --- CONFIGURATION ---
REVIEWS_CSV = "../data/raw/tabular/reviews.csv"
OUTPUT_TEXT_DIR = "../data/raw/texts/"

def clean_html(text):
    """Supprime les balises HTML simples comme <br/>."""
    if not isinstance(text, str):
        return ""
    # Expression régulière pour supprimer tout ce qui est entre < >
    return re.sub(r'<[^>]*>', ' ', text)

def ingest_texts():
    # 1. Vérification de la source
    if not os.path.exists(REVIEWS_CSV):
        print(f" Erreur : {REVIEWS_CSV} introuvable.")
        return

    print(" Lecture de reviews.csv en cours...")
    # On ne charge que les colonnes nécessaires pour économiser la RAM
    df = pd.read_csv(REVIEWS_CSV, usecols=['listing_id', 'comments'])
    
    # Supprimer les lignes sans commentaire
    df = df.dropna(subset=['comments'])

    # 2. Groupement par annonce
    print(" Regroupement des commentaires par ID d'annonce...")
    grouped = df.groupby('listing_id')

    total_listings = len(grouped)
    print(f"{total_listings} annonces avec commentaires détectées.")

    # 3. Création des fichiers individuels
    for listing_id, group in grouped:
        filename = f"{listing_id}.txt"
        filepath = os.path.join(OUTPUT_TEXT_DIR, filename)
        
        # PILIER : Idempotence (Optionnel ici, mais recommandé)
        if os.path.exists(filepath):
            continue

        try:
            # Récupération et nettoyage des commentaires
            comments_list = group['comments'].apply(clean_html).tolist()
            
            with open(filepath, "w", encoding="utf-8") as f:
                # En-tête strict selon le cahier des charges
                f.write(f"Commentaires pour l'annonce {listing_id}:\n")
                for comment in comments_list:
                    # On ajoute une puce pour chaque avis fusionné
                    f.write(f"* {comment.strip()}\n")
            
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier {listing_id}: {e}")

    print(f"\nIngestion texte terminée. {total_listings} fichiers créés dans /texts/.")

if __name__ == "__main__":
    # S'assurer que le dossier de sortie existe
    os.makedirs(OUTPUT_TEXT_DIR, exist_ok=True)
    ingest_texts()