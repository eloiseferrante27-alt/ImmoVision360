import pandas as pd
import os

# --- CONFIGURATION ---
# --- CONFIGURATION (Chemins corrigés) ---
CSV_PATH = "data/raw/tabular/listings.csv"
IMG_DIR = "data/raw/images/"
TXT_DIR = "data/raw/texts/"

TARGET_NEIGHBOURHOOD = "Élysée"

def run_audit():
    print("Lancement de l'audit de qualité du Data Lake...")

    # 1. Charger le référentiel théorique
    if not os.path.exists(CSV_PATH):
        print(f"Erreur : CSV introuvable à {CSV_PATH}")
        return

    df = pd.read_csv(CSV_PATH)
    # On isole les IDs que l'on DEVRAIT avoir
    df_elysee = df[df['neighbourhood_cleansed'] == TARGET_NEIGHBOURHOOD]
    expected_ids = set(df_elysee['id'].astype(str))
    total_expected = len(expected_ids)

    # 2. Scanner le contenu physique (ce qu'on a vraiment)
    # On récupère les noms de fichiers sans l'extension
    found_images = {f.split('.')[0] for f in os.listdir(IMG_DIR) if f.endswith('.jpg')}
    found_texts = {f.split('.')[0] for f in os.listdir(TXT_DIR) if f.endswith('.txt')}

    # 3. Calculer les statistiques
    img_success = expected_ids.intersection(found_images)
    txt_success = expected_ids.intersection(found_texts)

    img_rate = (len(img_success) / total_expected * 100) if total_expected > 0 else 0
    txt_rate = (len(txt_success) / total_expected * 100) if total_expected > 0 else 0

    # 4. Identifier les "Orphelins" (Annonces sans image)
    missing_images = expected_ids - found_images

    # --- AFFICHAGE DU RAPPORT ---
    print("\n" + "="*40)
    print(" RAPPORT DE SANTÉ - IMMOVISION 360")
    print("="*40)
    print(f" Quartier cible      : {TARGET_NEIGHBOURHOOD}")
    print(f" Annonces attendues  : {total_expected}")
    print("-" * 40)
    print(f" Images valides      : {len(img_success)} ({img_rate:.2f}%)")
    print(f"Textes valides      : {len(txt_success)} ({txt_rate:.2f}%)")
    print("-" * 40)
    
    if missing_images:
        print(f"Alerte : {len(missing_images)} images manquantes (URLs mortes ou erreurs DNS).")
        if len(missing_images) > 0:
            print(f" Exemple d'IDs manquants : {list(missing_images)[:5]}")
    else:
        print("Parfait : 100% de complétion !")
    
    print("="*40)

if __name__ == "__main__":
    run_audit()