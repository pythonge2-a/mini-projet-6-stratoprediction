[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/oOQR1xPR)
# StratoPrédiction

## Membres

- Welker Théo
- Melvi Isha
- Caputo Dany
- Imhof Valentin
- Laville Yanis

## Description

(Cf. README_Init.md)

## Cahier des charges

- Comprendre les données Grib puis télécharger les fichiers nécessaire.
- Rechercher un moyen d'importer ces fichiers avec Python
- Structurer ces données afin d'avoir accès rapidement aux informations
- Créer une fonction d'interpolation pour obtenir un vecteur V à la position souhaitée (Latitude, Longitude et Altitude)
- Fonction itérative pour faire naviguer un point du sol jusqu'au point d'explosiion puis la chute jusqu'à 0m
- Recherche d'une librairie permettant d'afficher ces points en 3D
- Recherche un moyen d'afficher ces points sur une carte
Fonctions supplémentaires en cas de temps à disposition: 
-Système en pyhton pour télécharger automatiquement les fichiers Grib
-Interpolation en 4D avec la gestion du temps inter-fichier
## Installation

```bash
poetry install
...
```

## (Pour les étudiants, à supprimer une fois fait)

### Comment créer le module

1. Créer un nouveau répertoire avec le nom du module
2. Créer un fichier `__init__.py` vide
3. Créer un fichier `__main__.py` vide
4. Mettre à jour le fichier `README.md`
5. Créer un projet Poetry avec `poetry new`
6. Ajouter les fichiers à Git
7. Commit et push
