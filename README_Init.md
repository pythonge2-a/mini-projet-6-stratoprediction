# StratoPrediction
Utilisation des données NOAA (Vent) pour la prédiction d'un parcout de vol d'un ballon stratosphérique. Pour remettre en contexte le besoin d'un tel système. Les ballons stratosphériques sont utilisés quotidiennement pour la récolte de donné météorologique ainsi que d'autres expériences dans la stratosphère. Le vol du ballon est dit "Libre" car il n'a aucune moyen de naviguer dans l'espace. Il subit obligatoirement les vents et se laisse guider librement. Un système de prédition est intéressant afin de connaitre approximativement le point de chute afin d'éviter les lacs où les montagnes. Certains vols enmènent de l'équipement onéreux et il est nécessaire d'assurer un parcout convenable. Il sera ainsi possible de modifier la date de décollage ou les paramètres de vols (vitesse ascentionelle, etc) pour modifier la trajectoire.

# But du projet

Développer un système de prédiction de vol de ballon stratosphérique. National Oceanic and Atmospheric Administration (NOAA) fournit énormément de donnée météo ainsi que des prédictions. Ces informations sont disponibles sur leur serveur et téléchargeable facilement. Leurs fichiers utilisent un format de fichier type "GRIB". Parmis ces fichiers, on trouve des prédictions de vents jusqu'à 10 jours dans le future. Les fichiers sont fractionnés par heure dans le futur mais possèdent chacun toutes les données de vecteur de vent du monde. Si on veut obtenir l'ensemble de ces données, il faudra plus de 6 Go à télécharger. Il existe plusieurs résolution de donnée, 0.25° / 0.5° ou 1° de longitude / latitude ce qui crée une matrice de donnée carré plus ou moins grande. Il est cependant possible de télécharger qu'une région de la planète grâce à leur outils de gestion de donnée

La première phase du projet est de comprendre ces données et d'arriver à les lire en python. (Le téléchargement des fichiers Grib2 peut se faire manuellement dans un premier temps)

Dès que les données sont intégrées, il sera possible de faire naviguer un point parmis les vecteurs de vents présent dans le fichier de prédiction (Grib). Dans ce fichier, on devrait normalement trouver la latitude, longitude, l'altitude ainsi qu'un vecteur vent (V, W). Par itération, le point (ballon stratosphérique) doit avancer dans ces vecteurs. A noter qu'il aura un vitesse ascentionelle constante d'environ 5 m/s et une explosion théorique à 32'000m. Pour bien faire, le point de départ devrait être au centre des données téléchargées. Comme la matrice de vent n'est donnée que pour max 0.25° d'angle de l'atitude et longitude, il sera nécessaire d'interpoler les vecteurs afin d'obtenir celui où se trouve le point à l'instant "t". Dans un premier temps, utiliser simplement un fichier "Grib" sans interpoler dans le temps. Car oui, il faut interpoler en 3D (latitude, longitude, altitude) ce qui sera déjà assez complexe. Si le temps du projet le permet, vous pourrait ensuite interpoler entre plusieurs fichier Grib. On peut imaginer créer une parcourt avec une infinité de point en faisant des sauts de cm en cm mais pour simplifier le temps de process, faite en sorte d'avoir un saut paramétrable et commencer avec des sauts de 1km par exemple. A la fin de cette partie, vous devriez avoir une liste de point dans l'espace. 

La dernière partie de projet consiste à présenter premièrement ces points dans un chart 3D libre de choix et ensuite de pouvoir les avoir sur une carte avec l'affichage de l'altitude pour chaque point.

# NOAA Data

Les données de vents sont disponibles : https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.20241128/12/atmos/

https://www.nco.ncep.noaa.gov/pmb/products/gfs/#GFS

gfs.t%02iz.pgrb2%s.0p50.f%03i
gfs.t12z.pgrb2.1p00.f000

https://github.com/cuspaceflight/tawhiri-downloader/blob/master/download.ml


Serveur de preconfiguration de région 

https://nomads.ncep.noaa.gov/
https://nomads.ncep.noaa.gov/gribfilter.php?ds=gfs_0p25

# Utilitaire pour visionner les fichiers

Il est possible de voir ces données en utilisant le logiciel XYGrib https://opengribs.org/en/xygrib

# Interprétation des fichiers Grib

<b>Chercher un moyen en pyhton de lire les fichiers Grib / Grib2 </b><br />
NOAA fournit un logiciel en c à compiler pour la plaftorm souhaité. : https://github.com/NOAA-EMC/wgrib2


# Résumer des tâches

1. Comprendre les données Grib puis télécharger les fichiers nécessaire.
2. Rechercher un moyen d'importer ces fichiers avec Python
3. Structurer ces données afin d'avoir accès rapidement aux informations
4. Créer une fonction d'interpolation pour obtenir un vecteur V à la position souhaitée (Latitude, Longitude et Altitude)
5. Fonction itérative pour faire naviguer un point du sol jusqu'au point d'explosiion puis la chute jusqu'à 0m
6. Recherche d'une librairie permettant d'afficher ces points en 3D
7. Recherche un moyen d'afficher ces points sur une carte

Fonctions supplémentaires en cas de temps à disposition
1. Système en pyhton pour télécharger automatiquement les fichiers Grib
2. Interpolation en 4D avec la gestion du temps inter-fichier








