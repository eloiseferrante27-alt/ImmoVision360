# ImmoVision360 Data Lake

Projet de collecte, préparation et chargement de données Airbnb sur le quartier **Élysée** à Paris.

L'objectif est d'alimenter une analyse autour de trois hypothèses :
- concentration de l'offre entre les mains de quelques hôtes ;
- professionnalisation de l'expérience locative ;
- standardisation visuelle et narrative des annonces.

## Structure
- `data/raw/tabular/listings.csv` : source tabulaire brute
- `data/raw/images/` : photos principales collectées
- `data/raw/texts/` : corpus textuel agrégé à partir des avis
- `data/processed/filtered_elysee.csv` : sous-ensemble extrait
- `data/processed/transformed_elysee.csv` : dataset enrichi pour la phase Silver
- `scripts/04_extract.py` : extraction ciblée
- `scripts/05_transform.py` : nettoyage et enrichissement
- `scripts/06_load.py` : chargement PostgreSQL

## Etat actuel du pipeline
- zone Bronze auditée sur 2625 annonces du quartier Élysée ;
- 1809 images valides détectées ;
- 1965 fichiers texte disponibles ;
- extraction régénérée sur 25 colonnes métier ;
- transformation régénérée sur 35 colonnes prêtes pour la zone Silver ;
- 778 annonces repérées comme visuellement standardisées par le score local ;
- 167 annonces repérées comme davantage "hôtelisées" par le score textuel ;
- pipeline de transformation rendu exécutable sans dépendre d'un appel IA externe ;
- chargement SQL prévu dans la table `elysee_listings_silver`.

## Ordre d'exécution
```bash
python scripts/03_sanity_check.py
python scripts/04_extract.py
python scripts/05_transform.py
python scripts/06_load.py
```

## Remarque méthodologique
La colonne `price` du dataset source est vide sur le sous-ensemble Élysée. Le pipeline conserve cette colonne à titre documentaire, mais les analyses quantitatives doivent s'appuyer d'abord sur la disponibilité, le volume d'avis, la densité d'hôtes multi-annonces et les enrichissements produits en Silver.
