[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/oOQR1xPR)
# StratoPrédiction

## Membres

- Welker Théo
- Melvi Isha
- Caputo Dany
- Imhof Valentin
- Laville Yanis

## Répartiton des tâches
  
- Dany et Yanis:
  Conception et mise en œuvre de la logique permettant de traiter les arguments d'entrée du programme.
  Validation des arguments fournis par l'utilisateur et gestion des erreurs pour assurer une compatibilité avec les autres modules du projet.

- Isha et Théo:
  Analyse des fichiers GRIB pour extraire les données météorologiques nécessaires.
  Développement des algorithmes permettant de prédire la trajectoire du ballon en fonction des données.
  Implémentation d'une fonction d'interpolation pour calculer un vecteur de vent (V) à partir des coordonnées (latitude, longitude, altitude).
  Création d'une fonction itérative pour simuler la montée et la descente du ballon.

- Valentin:
  Développement des outils de visualisation :
    Représentation 3D (latitude, longitude, altitude) de la trajectoire.
    Représentation 2D de l'altitude en fonction du temps.
    Affichage de la trajectoire sur une carte interactive.
  

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
Cloner le projet
```bash
git clone https://github.com/pythonge2-a/mini-projet-6-stratoprediction.git
```
Se diriger dans le répertoire
```bash
cd mini-projet-6-stratoprediction/
```
Installer les dépendances
```bash
poetry install 
```

## Utiliser le projet
Créer un environnement virtuel
```bash
poetry shell 
```
Lancer le programme
```bash
poetry run strato_prediction/ #Et là, on se laisse porter
```