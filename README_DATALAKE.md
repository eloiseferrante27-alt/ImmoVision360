# README_DATALAKE

## Architecture retenue
Le projet suit une logique de Data Lake simplifiée en trois niveaux :

- **Bronze** : données brutes importées sans transformation lourde (`listings.csv`, images, textes)
- **Silver** : données filtrées, nettoyées et enrichies (`filtered_elysee.csv`, `transformed_elysee.csv`)
- **Gold** : couche analytique à produire ensuite dans les notebooks, rapports ou dashboards

## Zone Bronze
La zone Bronze regroupe :
- les annonces Airbnb exportées dans `data/raw/tabular/`
- les images téléchargées dans `data/raw/images/`
- les commentaires agrégés dans `data/raw/texts/`

Elle conserve le format d'origine pour garantir la traçabilité.

## Zone Silver
La zone Silver contient les jeux prêts pour l'analyse :
- `filtered_elysee.csv` : extraction géographique et sélection de variables métier
- `transformed_elysee.csv` : dataset nettoyé et enrichi avec des scores exploitables

## Gouvernance minimale
- identifiant unique : `id`
- quartier cible : `neighbourhood_cleansed = "Élysée"`
- scripts d'orchestration séparés par étape pour faciliter l'audit du TP
- documentation dédiée par étape (`README_EXTRACT`, `README_TRANSFORM`, `README_LOAD`)

## Limites connues
- disponibilité partielle des images et textes ;
- colonne `price` non renseignée dans le jeu source sur ce sous-ensemble ;
- enrichissements IA remplacés par un fallback local déterministe lorsque Gemini n'est pas activé.
