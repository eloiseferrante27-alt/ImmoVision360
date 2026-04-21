# README_LOAD

## But
Le script `06_load.py` charge `transformed_elysee.csv` dans PostgreSQL.

## Variables d'environnement attendues
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST` (optionnel, défaut `localhost`)
- `DB_PORT` (optionnel, défaut `5432`)
- `DB_NAME` (optionnel, défaut `immovision_db`)

## Table cible
- nom : `elysee_listings_silver`
- stratégie : `replace`

## Garanties ajoutées
- vérification de l'existence du fichier d'entrée ;
- erreur explicite si les identifiants PostgreSQL manquent ;
- structure exécutable via fonction `run_load()`.

## Usage
```bash
python scripts/06_load.py
```
