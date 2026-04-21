# README_TRANSFORM

## Objectif
Le script `05_transform.py` prépare `filtered_elysee.csv` pour la zone Silver.

## Nettoyage appliqué
- normalisation de `host_response_rate` en pourcentage numérique ;
- normalisation textuelle de `host_response_time` ;
- conservation de `price` avec création d'une version numérique `price_numeric` ;
- création d'un indicateur `price_missing` pour rendre explicite l'absence de prix.

## Enrichissements produits
- `host_response_rate_pct` : pourcentage numérique exploitable
- `host_response_time_score` : score ordinal de réactivité
- `image_available` : présence d'une image locale
- `text_available` : présence d'un corpus texte local
- `standardization_score` : score visuel déterministe basé sur l'image locale
- `neighborhood_impact` : score textuel basé sur des signaux de type hôtelisé vs voisinage naturel
- `transform_run_mode` : `local_heuristics` par défaut

## Pourquoi un mode heuristique local ?
Le projet prévoyait un enrichissement Gemini, mais cette dépendance est fragile pour un rendu de TP :
- modèle distant pouvant changer ;
- quota/API key non garantis ;
- exécution non reproductible hors ligne.

Le pipeline a donc été rendu **reproductible localement**. Il reste compatible avec un enrichissement IA ultérieur si nécessaire.

## Résultats attendus après exécution
- input : `data/processed/filtered_elysee.csv`
- output : `data/processed/transformed_elysee.csv`
- volume de sortie vérifié : `2625` lignes et `35` colonnes
- `price_missing` : `2625` lignes
- `image_available = True` : `1809` lignes
- `text_available = True` : `1965` lignes
- `standardization_score = 1` : `778` lignes
- `neighborhood_impact = 1` : `167` lignes
- finalité : table Silver prête pour EDA, dashboard ou chargement SQL
