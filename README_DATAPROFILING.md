# README_DATAPROFILING

## Périmètre profilé
Source : `data/raw/tabular/listings.csv` filtré sur `neighbourhood_cleansed = "Élysée"`

## Volume observé
- lignes : `2625`
- quartier unique : `Élysée`
- images présentes : `1809`
- textes présents : `1965`

## Variables clés
- `host_id` : identification de l'hôte
- `calculated_host_listings_count` : mesure de concentration
- `host_response_time` / `host_response_rate` : indices de professionnalisation
- `picture_url` + image locale : support de lecture visuelle
- corpus d'avis agrégés : support de lecture textuelle du voisinage

## Valeurs manquantes notables
- `price` : 2625 valeurs manquantes sur le sous-ensemble Élysée
- `reviews_per_month` : 660 valeurs manquantes
- `review_scores_rating` : 660 valeurs manquantes
- `host_response_rate` : valeurs manquantes partielles, converties ensuite en pourcentage numérique

## Conséquences sur le TP
- l'axe économique ne peut pas reposer sur `price` seul ;
- les colonnes de réputation et de disponibilité restent exploitables ;
- le pipeline Silver doit privilégier des enrichissements robustes et documenter les manques plutôt que supprimer massivement des lignes.
