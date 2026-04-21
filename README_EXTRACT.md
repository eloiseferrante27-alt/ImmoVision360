# README_EXTRACT

## Contexte
Le script `04_extract.py` isole les annonces du quartier **Élysée** et ne conserve que les variables utiles pour le TP.

## Logique d'extraction
Filtre géographique :
- `neighbourhood_cleansed == "Élysée"`

## Colonnes conservées
### Hypothèse 1 : concentration de l'offre
- `id`
- `host_id`
- `host_name`
- `calculated_host_listings_count`
- `availability_365`
- `number_of_reviews`
- `review_scores_rating`
- `reviews_per_month`

### Hypothèse 2 : professionnalisation du lien hôte-voyageur
- `host_response_time`
- `host_response_rate`
- `host_is_superhost`
- `host_identity_verified`
- `description`
- `neighborhood_overview`

### Hypothèse 3 : standardisation visuelle
- `picture_url`
- `property_type`
- `room_type`
- `accommodates`
- `latitude`
- `longitude`

## Variables de contexte gardées pour l'audit
- `listing_url`
- `last_scraped`
- `name`
- `neighbourhood_cleansed`
- `price`

## Résultat attendu
- input : `data/raw/tabular/listings.csv`
- output : `data/processed/filtered_elysee.csv`
- volume cible : `2625` lignes
- largeur cible : `25` colonnes si toutes les variables attendues sont présentes

## Choix méthodologique
Le script est volontairement tolérant : si une colonne attendue n'existe pas dans la source, elle est signalée mais l'extraction continue. Cela évite qu'un changement mineur du schéma casse tout le pipeline.
