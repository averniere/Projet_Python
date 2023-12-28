# Python ENSAE 2A

Ce dépôt GitHub s'inscrit dans le cadre d'un projet "Python pour la Data Science", réalisé en deuxième année à l'ENSAE  par Aurane Verrière, Hugo Capot et Killian Pliszczak.

## Structure du projet

La sortie des énergies fossiles, nécessaire à la transition énergétique, amène les ménages et les entreprises à consommer toujours davantage d'électricité.

L'objectif de notre projet est de prévoir la consommation électrique d'un ménage en France en fonction de la performance énergétique de son bâtiment, de la météo et du climat de la région, et de l'évolution du prix de l'énergie.

A cette fin, nous avons donc découpé notre travail en plusieurs étapes :

1. Récupération des données
	-
	- Utilisation de la bibliothèque BeautifulSoup pour extraire différentes données (Fichier *scrapping.py*) :
		- Températures de différentes stations météorologiques grâce au site [Info Climat](infoclimat.fr)
		- Données de population par départements et par années sur la période 2011-2021 grâce au site de l'[INSEE](insee.fr)
	- Téléchargement de données publiques (Notebook *Etude par adresse)*:
		- Consommation électrique des logements par adresse depuis le site d'Enedis
		- DPE pour les logements français depuis l'API disponible depuis data.gouv.fr
		- Consommation annuelle d'électricité par département depuis le site de l'agence [ORE](agenceore.fr)
		- Températures moyennes par départements depuis le site de l'[ODRE](opendata.reseaux-energies.fr)
	
2. Nettoyage et traitement des données des données
	-
	- Restructuration des données météorologiques pour en retirer des variables utiles (Fichier *scrapping.py*)
	- Choix des stations météorologiques d'intérêt (Notebook *Etude par adresse*)
	- Création de tableaux résumant les données utilisées (Notebook *Modelisation*)
3. Visualisation et analyse des données
	-
	- Description des données de consommation par l'utilisation de cartes (Fichier ?) et de graphiques (Notebook *Recuperation_des_donnees_AV*)
	- Description des données de températures moyennes par l'utilisation de cartes (Fichier ?) et de graphiques (Notebook *Recuperation_des_donnees_AV*)
	- Etude des corrélations entre les variables (Notebook *Modelisation*)
4. Modélisation
	-
	- Régressions sur différentes variables (Notebook *Modelisation*)
	



## Modules et packages nécessaire à l'exécution

Veuillez trouver ci-dessous les modules et packages nécessaires à la bonne exécution du projet. Pour plus de simplicité, vous les retrouverez aussi dans le fichier **requirement.txt**.

```bash
pip install -q lxml
pip  install  pandas
pip  install  geopandas
pip  install  lxml
pip  install  urllib
pip  install  matplotlib
pip  install  requests  py7zr  geopandas  openpyxl  tqdm  s3fs  PyYAML  xlrd
pip  install  git+https://github.com/inseefrlab/cartiflette@80b8a5a28371feb6df31d55bcc2617948a5f9b1a
pip  install  mapclassify
pip  install  folium
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