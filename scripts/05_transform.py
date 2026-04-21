from __future__ import annotations

import colorsys
import math
from pathlib import Path
import re
from typing import Iterable

import pandas as pd
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "data" / "processed" / "filtered_elysee.csv"
OUTPUT_CSV = BASE_DIR / "data" / "processed" / "transformed_elysee.csv"
IMG_DIR = BASE_DIR / "data" / "raw" / "images"
TXT_DIR = BASE_DIR / "data" / "raw" / "texts"

RESPONSE_TIME_MAP = {
    "within an hour": 4,
    "within a few hours": 3,
    "within a day": 2,
    "a few days or more": 1,
}

HOTEL_WORDS = {
    "concierge",
    "check-in",
    "check in",
    "self check",
    "cleaner",
    "house keeper",
    "professional",
    "team",
    "staff",
    "hotel",
    "air conditioning",
    "co-host",
}

LOCAL_WORDS = {
    "neighborhood",
    "neighbourhood",
    "quartier",
    "bakery",
    "boulangerie",
    "market",
    "marché",
    "family",
    "famille",
    "local",
    "parisian",
    "parisien",
    "park",
    "parc",
    "restaurants",
    "shops",
    "commerces",
    "at home",
    "comme à la maison",
}


def parse_price(value: object) -> float | None:
    if pd.isna(value):
        return None
    cleaned = re.sub(r"[^0-9.]+", "", str(value))
    return float(cleaned) if cleaned else None


def parse_response_rate(value: object) -> float | None:
    if pd.isna(value):
        return None
    cleaned = str(value).strip().replace("%", "")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().lower().split())


def image_path_for(listing_id: object) -> Path:
    return IMG_DIR / f"{listing_id}.jpg"


def text_path_for(listing_id: object) -> Path:
    return TXT_DIR / f"{listing_id}.txt"


def sample_pixels(image: Image.Image) -> Iterable[tuple[int, int, int]]:
    reduced = image.convert("RGB").resize((64, 64))
    width, height = reduced.size
    pixels = [
        reduced.getpixel((x, y))
        for y in range(0, height, 2)
        for x in range(0, width, 2)
    ]
    return pixels


def compute_standardization_score(listing_id: object) -> int:
    path = image_path_for(listing_id)
    if not path.exists():
        return -1

    try:
        with Image.open(path) as img:
            pixels = list(sample_pixels(img))
    except Exception:
        return -1

    if not pixels:
        return -1

    brightness_values = []
    saturation_values = []
    for r, g, b in pixels:
        rf, gf, bf = r / 255.0, g / 255.0, b / 255.0
        hue, saturation, value = colorsys.rgb_to_hsv(rf, gf, bf)
        brightness_values.append(value)
        saturation_values.append(saturation)

    avg_brightness = sum(brightness_values) / len(brightness_values)
    avg_saturation = sum(saturation_values) / len(saturation_values)
    variance = sum((value - avg_brightness) ** 2 for value in brightness_values) / len(brightness_values)
    contrast = math.sqrt(variance)

    if avg_brightness >= 0.63 and avg_saturation <= 0.25 and contrast <= 0.17:
        return 1
    if avg_brightness >= 0.55 and avg_saturation <= 0.18:
        return 1
    return 0


def load_review_text(listing_id: object) -> str:
    path = text_path_for(listing_id)
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="ignore").lower()
    except Exception:
        return ""


def compute_neighborhood_impact(listing_id: object) -> int:
    text = load_review_text(listing_id)
    if not text:
        return -1

    hotel_score = sum(text.count(word) for word in HOTEL_WORDS)
    local_score = sum(text.count(word) for word in LOCAL_WORDS)

    if hotel_score >= local_score + 2:
        return 1
    if local_score >= hotel_score + 2:
        return 0
    return -1


def run_transform() -> None:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"CSV introuvable: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    df["price_numeric"] = df["price"].apply(parse_price) if "price" in df.columns else None
    df["price_missing"] = df["price_numeric"].isna() if "price_numeric" in df.columns else True

    if "host_response_rate" in df.columns:
        df["host_response_rate_pct"] = df["host_response_rate"].apply(parse_response_rate)
        median_rate = df["host_response_rate_pct"].dropna().median()
        if pd.isna(median_rate):
            median_rate = 0.0
        df["host_response_rate_pct"] = df["host_response_rate_pct"].fillna(median_rate)
    else:
        df["host_response_rate_pct"] = 0.0

    if "host_response_time" in df.columns:
        df["host_response_time_normalized"] = df["host_response_time"].apply(normalize_text)
        df["host_response_time_score"] = (
            df["host_response_time_normalized"].map(RESPONSE_TIME_MAP).fillna(0).astype(int)
        )
    else:
        df["host_response_time_normalized"] = ""
        df["host_response_time_score"] = 0

    df["image_available"] = df["id"].apply(lambda listing_id: image_path_for(listing_id).exists())
    df["text_available"] = df["id"].apply(lambda listing_id: text_path_for(listing_id).exists())
    df["standardization_score"] = df["id"].apply(compute_standardization_score)
    df["neighborhood_impact"] = df["id"].apply(compute_neighborhood_impact)
    df["transform_run_mode"] = "local_heuristics"

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Transformation terminée vers: {OUTPUT_CSV}")
    print(f"Lignes: {df.shape[0]} | Colonnes: {df.shape[1]}")
    print(f"Images disponibles: {int(df['image_available'].sum())}")
    print(f"Textes disponibles: {int(df['text_available'].sum())}")
    print(f"Standardization score = 1: {int((df['standardization_score'] == 1).sum())}")
    print(f"Neighborhood impact = 1: {int((df['neighborhood_impact'] == 1).sum())}")


if __name__ == "__main__":
    run_transform()
