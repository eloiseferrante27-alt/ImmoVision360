from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "raw" / "tabular" / "listings.csv"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "filtered_elysee.csv"
TARGET_NEIGHBOURHOOD = "Élysée"

COLS_TO_KEEP = [
    "id",
    "listing_url",
    "last_scraped",
    "name",
    "description",
    "neighborhood_overview",
    "picture_url",
    "host_id",
    "host_name",
    "host_response_time",
    "host_response_rate",
    "host_is_superhost",
    "host_identity_verified",
    "calculated_host_listings_count",
    "neighbourhood_cleansed",
    "latitude",
    "longitude",
    "property_type",
    "room_type",
    "accommodates",
    "price",
    "availability_365",
    "number_of_reviews",
    "review_scores_rating",
    "reviews_per_month",
]


def run_extraction() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"CSV introuvable: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    df_filtered = df[df["neighbourhood_cleansed"].fillna("") == TARGET_NEIGHBOURHOOD].copy()

    available_columns = [column for column in COLS_TO_KEEP if column in df_filtered.columns]
    missing_columns = [column for column in COLS_TO_KEEP if column not in df_filtered.columns]

    df_final = df_filtered[available_columns].copy()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_PATH, index=False)

    print(f"Extraction terminée vers: {OUTPUT_PATH}")
    print(f"Lignes: {df_final.shape[0]} | Colonnes: {df_final.shape[1]}")

    if missing_columns:
        print("Colonnes absentes ignorées:", ", ".join(missing_columns))


if __name__ == "__main__":
    run_extraction()
