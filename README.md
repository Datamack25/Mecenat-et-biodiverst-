# Veille Outre-mer (Streamlit)
Fichiers à la racine du dépôt : `app.py`, `core.py`, `defaults.py`, `requirements.txt`. Si le dossier `data/` manque, l'app le recrée automatiquement.

## Lancer en local
```
pip install -r requirements.txt
streamlit run app.py
```
## Déployer (gratuit) sur Streamlit Community Cloud
1. Uploadez ce dossier (dossier `.github` inclus) dans un dépôt GitHub.
2. Allez sur share.streamlit.io → New app → choisissez le dépôt, branche `main`, fichier `app.py`.
3. Optionnel : Settings → Secrets → `ANTHROPIC_API_KEY = "sk-..."` pour l'enrichissement par IA.
## Persistance
Sur Streamlit Cloud, les fichiers écrits depuis l'app (bouton Actualiser, ajout de terme) ne sont pas conservés après redémarrage. Le workflow GitHub Actions quotidien (`.github/workflows/update.yml`) met à jour `data/` dans le dépôt : activez Settings → Actions → General → « Read and write permissions », ajoutez le secret `ANTHROPIC_API_KEY` dans les secrets Actions, puis lancez-le une première fois (Run workflow).

## Nouveautés
- Encyclopédie : 70 termes (`data/encyclopedie.csv`), enrichie par le bouton de mise à jour.
- Onglets Lectures, Territoires (`data/geographie.csv`), Emplois, Réglementation et boîtes à outils (mécénat, DPEF).
- Exports PDF : un par onglet de la page (section « Exports PDF ») et un par boîte à outils.
- Dépendance ajoutée : `reportlab` (déjà dans `requirements.txt`).

## Version 3.0
Site entièrement rendu par Streamlit (plus d'iframe : plus d'espace blanc). Menu en haut, page « Boîtes à outils » dédiée, administration dans le volet gauche (flèche verte en haut à gauche), version affichée dans le pied de page.

## Version 3.1
Menu simplifié (8 pages). Nouveau : « Fondations & acteurs » (fondations biodiversité/insertion, veille mécénat de compétences) et onglet « Philanthropie & mécénat » dans Emplois. Données dans `content.py`.
