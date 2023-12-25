# Import des librairies
import bs4
#import lxml
import pandas as pd
import urllib
import cartiflette.s3 as s3
from urllib import request
import os
from os.path import isfile
import requests

### URL utiles ###
# Données météo par communes et département
url_soleil="https://static.data.gouv.fr/resources/donnees-du-temps-densoleillement-par-departements-en-france/20221207-142648/temps-densoleillement-par-an-par-departement-feuille-1.csv"

api_root_temp="https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/temperature-quotidienne-departementale/records"
api_req_tmoy="?select=avg(tmoy)&group_by=code_insee_departement%2C%20departement"
api_req_tmin="?select=min(tmin)&group_by=code_insee_departement%2C%20departement"
api_req_tmax="?select=max(tmax)&group_by=code_insee_departement%2C%20departement"

# Données de consommation d'électricité par adresses et par départements
consumption_data_url_2018="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222018%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
consumption_data_url_2019="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222019%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
consumption_data_url_2020="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222020%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
consumption_data_url_2021="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222021%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

cons_département="https://opendata.agenceore.fr/api/explore/v2.1/catalog/datasets/conso-elec-gaz-annuelle-par-secteur-dactivite-agregee-departement/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"


### Importation des données météo ###
class Meteo :
    def __init__(self):
        self.data_all = {i : {j : {} for j in range(1,13)} for i in range(2011,2019)}

    def scrap(self):
        for y in self.data_all :
            for m in self.data_all[y] :
                url_test = 'https://www.infoclimat.fr/stations-meteo/analyses-mensuelles.php?mois=' + str(m) + '&annee=' + str(y)
                raw_text = request.urlopen(url_test).read()
                page = bs4.BeautifulSoup(raw_text,'lxml')
                tableau = page.find('table', {'id' : 'tableau-releves'})
                rows = tableau.find_all('tr')
                df = {'Villes' : [rows[i].find('a').text for i in range(1,len(rows))],
                      'Température minimale extrême du mois' : [rows[i].find('div').text for i in range(1,len(rows))],
                      'Moyenne des températures minimales du mois' : [rows[i].find_all('td')[2].text for i in range(1,len(rows))],
                      'Température moyenne du mois' : [rows[i].find_all('td')[3].text for i in range(1,len(rows))],
                      'Moyenne des températures maximales du mois' : [rows[i].find_all('td')[4].text for i in range(1,len(rows))],
                      'Température maximale extrême du mois' : [rows[i].find_all('td')[5].find('div').text for i in range(1,len(rows))],
                      'Cumul de précipitation du mois' : [rows[i].find_all('td')[6].text for i in range(1,len(rows))],
                      "Heure d'ensoleillement du mois" : [rows[i].find_all('td')[7].text for i in range(1,len(rows))],
                      'Rafale maximale du mois' : [rows[i].find_all('td')[8].text for i in range(1,len(rows))]
                      }
                
                self.data_all[y][m] = df
    
        def export(self):
            self.df_all = pd.DataFrame(self.data_all)
            self.df_all.to_json('data_base.json')
    
        def rename(self):
            self.df_all = pd.DataFrame(self.data_all)
            self.df_all.rename({'Villes' : 'ville',
               'Température minimale extrême du mois' : 'tnn',
               'Moyenne des températures minimales du mois' : 'tnm', 
               'Température moyenne du mois' : 'tmm',
               'Moyenne des températures maximales du mois' : 'txm',
               'Température maximale extrême du mois' : 'txx',
               'Cumul de précipitation du mois' : 'rr',
               "Heure d'ensolleiment du mois" : 'ens',
               'Rafale maximale du mois' : 'rafale'}, axis=1, inplace = True)


### Importation des données de consommation ###
def df_filter(df, wanted_variables):
    ''' 
    Retourne un dataframe avec les seules variables que l'on souhaite conserver.
    Args: 
        df (DataFrame)
        wanted_variables (list)
    Returns: the dataframe with only the variables needed
    '''
    return df[wanted_variables]
   
def get_data_consumption(url, year, replace:bool = False):
    '''Charge les données de consommation d'électricité du secteur résidentiel par adresse pour une année
     donnée
    Entrées:
        url(string)
        year(string)
        replace(bool): True si l'on souhaite remplacer consommation{year}.csv si le fichier existe/False par défaut
    Sortie: 
        df (dataframe) 
    '''
    path_to_data="consommations\consommation"+f"{year}"+".csv"
    if (isfile(path_to_data) and not replace):
        df=pd.read_csv(path_to_data, sep=";")
    else:
        print("Chargement des données, cette étape peut prendre quelques minutes")
        response=requests.get(url)
        if response.status_code == 200:
            with open(path_to_data, "wb") as file:
                file.write(response.content)
            print("Téléchargement réussi.")
        else:
            print(f"Échec du téléchargement. Code d'état : {response.status_code}")
        df=pd.read_csv(path_to_data, sep=";")
    return df

def get_data_consumption_department(df, year):
    '''Récupère les données de consommation annuelle d'électricité par département pour une année donnée
    Entrées:
        df (DataFrame)
        year (string)
    Sortie:
        df (DataFrame)
    '''
    df_year= df[(df["Année"]==year) & (df["Filière"]=="Electricité")]
    return df_year


### Importation des données de températures à l'échelle des départements ###
def get_data_from_api(api_root, api_req, année):
    ''' Récupère des données à partir d'une API et d'une requête précise.
    Entrées: 
        api_root (string) : url "racine" de l'API 
        api_req (string) : bout d'url indiquant la requête précise que l'on souhaite effectuer 
        année (float) : année des données que l'on veut récupérer
    Sortie:
        df (DataFrame) 
    '''
    api_url=f"{api_root}"+f"{api_req}"+"&refine=date_obs%3A%22"+f"{année}%22"
    req=requests.get(api_url)
    wb=req.json()
    df=pd.json_normalize(wb["results"])
    return df 


### Fonds de cartes ###
dep = s3.download_vectorfile_url_all(
    values = "metropole",
    crs = 4326,
    borders = "DEPARTEMENT",
    vectorfile_format="topojson",
    filter_by="FRANCE_ENTIERE",
    source="EXPRESS-COG-CARTO-TERRITOIRE",
    year=2022) # Fond de carte des départements français 

var_dep=['NOM','INSEE_DEP', 'geometry'] # On ne garde que les variables codant le code du département et la variable geometry

def save_map(m, choropleth, year, format, replace:bool=False):
    '''Enregistre une carte dans le dossier cartes du repository.
    Entrées:
            m (): fond de carte
            choropleth(): attributs de la carte choroplèthe à supperposer au fond de carte
            year (string): 
    '''
    path_to_map="cartes\carte_temp"+f"{year}"+"."+f"{format}"
    if not (isfile (path_to_map) and not replace):
        choropleth.add_to(m)
        m.save(path_to_map)
