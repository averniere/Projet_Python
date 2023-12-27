# Python ENSAE 2A

Ce dépôt GitHub s'inscrit dans le cadre d'un projet "Python pour la Data Science", réalisé en deuxième année à l'ENSAE  par Aurane Verrière, Hugo Capot et Killian Pliszczak.

## Structure du projet

La sortie des énergies fossiles, nécessaire à la transition énergétique, amène les ménages et les entreprises à consommer toujours davantage d'électricité.

L'objectif de notre projet est de prévoir la consommation électrique d'un ménage en France en fonction de la performance énergétique de son bâtiment, de la météo et du climat de la région, et de l'évolution du prix de l'énergie.

A cette fin, nous avons donc découpé notre travail en plusieurs étapes :

1. Récupération des données
	-
	- Utilisation de la bibliothèque BeautifulSoup pour extraire des différentes données :
		- Températures de différentes stations météorologique grâce au site infoclimat.fr
		- Données de population par départements et par années sur la période 2011-2021 grâce au site insee.fr
	- Téléchargement de données publiques :
		- X
		- X
		- X
	
2. Nettoyage et traitement des données des données
	-
	- Restructuration des données météorologique pour en retirer des variables utiles
	- 
3. Visualisation et analyse des données
	-
	-
4. Modélisation
	-

## Modules et packages nécessaire à l'exécution

Veuillez trouver ci-dessous les modules et packages nécessaires à la bonne exécution du projet. Pour plus de simplicité, vous les retrouverez aussi dans le fichier **requirement.txt**.

`pip install -q lxml`
`import bs4`
`import lxml`
`import pandas`
`import urllib`
`from tqdm.auto import tqdm`
`from urllib import request`
`import pandas as pd`
`import numpy as np`