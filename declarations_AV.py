# Import des librairies
import bs4
import lxml
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
    """
    Class permettant de scrapper et d'effectuer des opérations sur les données d'Infoclimat concernant la température observée par différentes 
    stations météo.
    """
    def __init__(self):
        """
        Initialisation de la class contenant :
            self.année_début : int
                Année de début des données qu'on souhaite scrapper
            self.année_fin : int
                Année de fin des données qu'on souhaite scrapper
            self.data_all : dict
                Contient l'ensemble des données par année (initialement vides)
        """
        #Par défaut, on cadre notre extraction de données entre 2018 et 2021, années pour lesquelles nous avons des données de consommation
        self.année_début=2018 
        self.année_fin=2021
        self.data_all = {i : {j : {} for j in range(1,13)} for i in range(self.année_début,self.année_fin+1)}

    def scrap(self):
        """
        Fonction permettant de scrapper les données voulues, i.e. les données d'infoclimat concernant la température observée par différentes 
        stations météo entre 2011 et 2018, avec un pré-tri permettant d'éviter toute répétition de ville au sein d'un même mois.

            Paramètres:
            ------------
                self.data_all : dict
                    Dictionnaire contenant toutes les données par années
        
            Output:
            ----------
                self.data_pop : dict
                    Dictionnaire contenant toutes les données par années actualisées
            
        """
        #On boucle sur toutes les années souhaitées
        for y in self.data_all :
            #On boucle ensuite sur tous les mois de l'année
            for m in self.data_all[y] :
                url_temp = 'https://www.infoclimat.fr/stations-meteo/analyses-mensuelles.php?mois=' + str(m) + '&annee=' + str(y)
                raw_text = request.urlopen(url_temp).read()
                page = bs4.BeautifulSoup(raw_text,'lxml')
                tableau = page.find('table', {'id' : 'tableau-releves'})
                rows = tableau.find_all('tr')
                
                #On stocke les données d'un mois et d'une année dans un dictionnaire
                df = {
            'ville' : [rows[i].find('a').text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            'tnn' : [rows[i].find('div').text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            'tnm' : [rows[i].find_all('td')[2].text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            'tmm' : [rows[i].find_all('td')[3].text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            'txm' : [rows[i].find_all('td')[4].text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            'txx' : [rows[i].find_all('td')[5].find('div').text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            'rr' : [rows[i].find_all('td')[6].text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            "ens" : [rows[i].find_all('td')[7].text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text],
            'rafale' : [rows[i].find_all('td')[8].text for i in range(1,len(rows)) if rows[i].find('a').text!=rows[i-1].find('a').text] 
                    }
                #La condition "if" dans toutes les listes permet de nous assurer que nous ne prenons qu'une seule donnée par ville
                #Par défaut, si cette ville est renseignée deux fois, nous ne prenons que la première information
                #Ceci nous permet d'éviter les répétitions de villes, qui bruitent la suite
               
                self.data_all[y][m] = df

    def export(self):
        """
        Fonction intégrée d'export au format DataFrame et au format .json
        pour permettant de faciliter les manipulations.
        Cette méthode ne sera pas utilisée en pratique dans notre projet

        Paramètres:
        ------------
            self.data_pop : dict
                Dictionnaire contenant toutes les données par années
        
        Output:
        ----------
            Aucun
        """
        
        self.df_all = pd.DataFrame(self.data_all)
        self.df_all.to_json('data_base.json')

    def liste_min(self, year):
        """
        Comme les stations ne sont pas les mêmes d'un mois à l'autre,
        cette fonction permet, pour une année donnée, de construire la liste des stations communes 
        à tous les mois pour une année donnée.

        Entrée:
        ------------
            year : int
                Année qui nous intéresse. Elle doit être entre self.année_début=2018 et self.année_fin

        Paramètres:
        ------------
            self.data_all : dict
                Dictionnaire contenant toutes les données par années
        
        Output:
        ----------
            intersection : list
                liste des stations communes à tous les mois pour une année donnée.
        """
        intersection=self.data_all[year][1]['ville']
        for m in range(2,13):
            intersection=[x for x in intersection if x in self.data_all[year][m]['ville']]
        return intersection

    def dico_minimal(self,year) :
        """
        Cette fonction construit le dictionnaire des données pour chaque mois d'une année "year" donnée, 
        mais seulement pour les villes proposant des données pour tous les mois de l'année.

        Entrée:
        ------------
            year : int
                Année qui nous intéresse. Elle doit être entre self.année_début=2018 et self.année_fin

        Paramètres:
        ------------
            self.data_all : dict
                Dictionnaire contenant toutes les données par années
            self.list_min : function
                Méthode de la classe Meteo qui renvoie la liste des villes communes à tous les mois 
                pour une année donnée
        
        Output:
        ----------
            df_min : dict
                dictionnaire des données pour chaque mois d'une année "year" donnée, 
                mais seulement pour les villes pour lesquelles on a des données pour tous les mois
        """
        intersection = self.liste_min(year)
        df_min={j : {} for j in range(1,13)}
        for m in range (1,13):
            df={'ville':[],'tnn':[],'tnm':[],'tmm':[],'txm':[],'txx':[],'rr':[],"ens":[],'rafale':[]}
            for i in range (len(self.data_all[year][m]['ville'])):
                if self.data_all[year][m]['ville'][i] in intersection and self.data_all[year][m]['ville'][i] != self.data_all[year][m]['ville'][i-1]: 
                    df['ville'].append(self.data_all[year][m]['ville'][i])
                    df['tnn'].append(self.data_all[year][m]['tnn'][i])
                    df['tnm'].append(self.data_all[year][m]['tnm'][i])
                    df['tmm'].append(self.data_all[year][m]['tmm'][i])
                    df['txm'].append(self.data_all[year][m]['txm'][i])
                    df['txx'].append(self.data_all[year][m]['txx'][i])
                    df['rr'].append(self.data_all[year][m]['rr'][i])
                    df['ens'].append(self.data_all[year][m]['ens'][i])
                    df['rafale'].append(self.data_all[year][m]['rafale'][i])
            df_min[m]=df       
        return df_min
        
        

    def tableau_annuel(self,year):
        """
        Fonction intégrée d'export en data frame des données météo sous forme de moyenne pour une année.
        Il faut que cette année "year" ait été importée, c'est-à-dire qu'elle soit 
        entre self.année_début et self.année_fin

        Paramètres:
        ------------
            self.dico_minimal(year) : dict
                Dictionnaire contenant toutes les données par mois pour les stations aux données fournies
                pour toute l'année
            self.dico_minimal(year) : list
                Liste des stations offrant des données pour toute l'année
        
        Output:
        ----------
            data : DataFrame
        """
        dico_min=self.dico_minimal(year)
        L=self.liste_min(year)
        df={j : {} for j in ['ville','tnn','tnm','tmm','txm','txx','rr','ens','rafale']}
        for x in range(len(L)):
            df['ville'][x]=L[x]
        for j in ['tnn','tnm','tmm','txm','txx','rr','ens','rafale']:
            dico={ville : [] for ville in L} 
            for x in range(len(L)):
                for m in range(1,13):
                    u=0
                    if dico_min[m][j][x]!='':
                        u+=1
                        dico[L[x]].append(float(dico_min[m][j][x]))
                    if u==0 :
                        moyenne='Rien'
                    else :
                        moyenne = sum(dico[L[x]])/u
                df[j][x]=moyenne
        data= pd.DataFrame(df)
        data.rename({'ville' : 'Villes', 
            'tnn' : 'Moyenne des températures minimales extrêmes (\mois)',
            'tnm' : 'Moyenne des moyennes des températures minimales (\mois)', 
            'tmm' : 'Moyennes des température moyennes (\mois)', 
            'txm' : 'Moyenne des moyennes des températures maximales (\mois)', 
            'txx' : 'Moyenne des températures maximales extrêmes (\mois)', 
            'rr' : 'Moyenne des cumuls de précipitation (\mois)', 
            'ens' : "Moyenne des heures d'ensoleillement (\mois)", 
            'rafale' : 'Moyenne des rafales maximales (\mois)'},axis=1,inplace = True)
        return(data)
        

    def rename_pratique(self):
        """
        Fonction intégrée permettant de renommer facilement les colonnes par le nom utilisé par Infoclimat dans le but de faciliter le traitement.

        Paramètres :
        ------------
            self.df_all : DataFrame
                DataFrame contenant toutes les données météo extraites

        Output :
        --------
            self.df_all : DataFrame
                DataFrame contenant les mêmes données mais dont les colonnes ont été renommées
        """
        
        self.df_all = pd.DataFrame(self.data_all)
        self.df_all.rename({'Villes' : 'ville', 
           'Température minimale extrême du mois' : 'tnn',
           'Moyenne des températures minimales du mois' : 'tnm', 
           'Température moyenne du mois' : 'tmm', 
           'Moyenne des températures maximales du mois' : 'txm', 
           'Température maximale extrême du mois' : 'txx', 
           'Cumul de précipitation du mois' : 'rr', 
           "Heure d'ensoleillement du mois" : 'ens', 
           'Rafale maximale du mois' : 'rafale'},axis=1,inplace = True)

    def rename_esthétique(self):
        """
        Fonction intégrée permettant de renommer facilement les colonnes par leur véritable nom, après les avoir simplifié.

        Paramètres :
        ------------
            self.df_all : DataFrame
                DataFrame contenant toutes les données météo extraites

        Output :
        --------
            self.df_all : DataFrame
                DataFrame contenant les mêmes données mais dont les colonnes ont été renommées
        """
        
        self.df_all = pd.DataFrame(self.data_all)
        self.df_all.rename({'ville' : 'Villes', 
            'tnn' : 'Température minimale extrême du mois',
            'tnm' : 'Moyenne des températures minimales du mois', 
            'tmm' : 'Température moyenne du mois', 
            'txm' : 'Moyenne des températures maximales du mois', 
            'txx' : 'Température maximale extrême du mois', 
            'rr' : 'Cumul de précipitation du mois', 
            'ens' : "Heure d'ensoleillement du mois", 
            'rafale' : 'Rafale maximale du mois'},axis=1,inplace = True)


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
    '''Enregistre une carte Folium dans le dossier cartes du repository.
    Entrées:
            m (): fond de carte
            choropleth(): attributs de la carte choroplèthe à supperposer au fond de carte
            year (string): 
    '''
    path_to_map="cartes\carte_temp"+f"{year}"+"."+f"{format}"
    if not (isfile (path_to_map) and not replace):
        choropleth.add_to(m)
        m.save(path_to_map)