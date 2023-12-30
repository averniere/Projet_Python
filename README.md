# Python ENSAE 2A

Ce dépôt GitHub s'inscrit dans le cadre d'un projet "Python pour la Data Science", réalisé en deuxième année du cycle ingénieur de l'ENSAE par Aurane Verrière, Hugo Capot et Killian Pliszczak.

## Etapes du projet

En engendrant un réchauffement global de l'atmosphère, le dérèglement climatique actuel, amène les ménages à modifier leur consommation. Identifier les déterminants de ces comportements devient donc un point crucial, tant pour les exploitants que les gouvernants.

L'objectif de notre projet est de prévoir la consommation électrique d'un ménage en France en fonction de la performance énergétique de son bâtiment, de la météo et du climat de la région. Notre étude se fait à deux échelles : la prévision de la consommation électrique départementale dans un premier temps, puis la prévision de la consommation adresse par adresse.

A cette fin, nous avons donc découpé notre travail en plusieurs étapes :

1. Récupération des données
	-
	- Utilisation de la bibliothèque BeautifulSoup pour extraire différentes données (Fichier *declarations.py* et Notebook *Scrapping_Population*) :
		- Températures de différentes stations météorologiques grâce au site [Info Climat](https://www.infoclimat.fr/stations-meteo/analyses-mensuelles.php?mois=12&annee=2021)
		- Données de population par départements et par années sur la période 2011-2021 grâce au site de l'[INSEE](https://www.insee.fr/fr/statistiques/3677771?sommaire=3677855)
   - Téléchargement de données publiques (Notebooks *Etude par adresse* et *Récupération_des_données*):
		- Consommation électrique des logements par adresse depuis le site d'[Enedis](https://data.enedis.fr/pages/accueil/)
		- DPE pour les logements français depuis l'API disponible depuis data.gouv.fr
		- Consommation annuelle d'électricité par département depuis le site de l'agence [ORE](agenceore.fr)
		- Températures moyennes par départements depuis le site de l'[ODRE](opendata.reseaux-energies.fr)
	
2. Nettoyage et traitement des données des données
	-
	- Restructuration des données météorologiques pour en retirer des variables utiles (Notebook *Etude par adresse*)
	- Choix des stations météorologiques d'intérêt (Notebook *Etude par adresse*)
	- Choix de villes d'intérêt pour notre étude (Notebook *Etude par adresse*)
	- Restructuration des données de consommation à l'échelle départementale et communale (Notebooks *Modelisation* et *Etude_par_adresse*)
3. Visualisation et analyse des données
	-
	- Description des données de consommation par l'utilisation de cartes et de graphiques (Notebook *Recuperation_des_donnees*)
	- Description des données de températures moyennes par l'utilisation de cartes et de graphiques (Notebook *Recuperation_des_donnees*)
	- Etude des corrélations entre les variables (Notebook *Modelisation*)
4. Modélisation
	-
	- Régressions sur différentes variables (Notebook *Modelisation*)
	- Conclusions
	

## Structure du répertoire 

Sont présents dans ce répertoire différents fichiers ayant des objectifs complémentaires. Nous proposons ici un ordre de parcours indicatif :
	
	I. 	declarations.py
	II. Etude à l'échelle départementale :
		- recuperation_des_donnees.ipynb
		- Scrapping_population.ipynb
        - Carte_ensoleillement.ipynb
		- Modelisation.ipynb
	III. Etude de la consommation par adresse :
		- Etude_par_adresse.ipynb


## Modules et packages nécessaire à l'exécution

Veuillez trouver ci-dessous les modules et packages nécessaires à la bonne exécution du projet. Pour plus de simplicité, vous les retrouverez aussi dans le fichier **requirement.txt**.

```bash
pip install -q lxml
pip install  pandas
pip install  geopandas
pip install  lxml
pip install  urllib
pip install  matplotlib
pip install  requests  py7zr  geopandas  openpyxl  tqdm  s3fs  PyYAML  xlrd
pip install  git+https://github.com/inseefrlab/cartiflette@80b8a5a28371feb6df31d55bcc2617948a5f9b1a
pip install  mapclassify
pip install  folium
pip install import-ipynb
pip install seaborn
pip install statsmodels
```

```Python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import bs4
import lxml
import urllib
from tqdm.auto import tqdm
from urllib import request
import declarations as dec
import importlib
import requests
import geopandas as gpd
import declarations_AV as dec
import matplotlib.pyplot as plt
import mapclassify as mc
import folium
import os
from os.path import isfile
import json
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sklearn.metrics
from sklearn import preprocessing
import statsmodels.api as sm
import statsmodels.formula.api as smf
```