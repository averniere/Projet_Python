!pip install -q lxml

""" Importation des packages """

import bs4
import lxml
import pandas
import urllib
from tqdm.auto import tqdm

from urllib import request

class Meteo :
    """
    Class permettant de scrapper et d'effectuer des opérations sur les données d'infoclimat concernant la température observée par différentes 
    stations météo entre 2011 et 2018.
    """
    def __init__(self):
        """
        Initialisation de la class contenant :
            self.data_all : dict
                Contient l'ensemble des données par année (initialement vides)
        """
        self.data_all = {
                i : {j : {} for j in range(1,13)} for i in range(2011,2019)
            }

    def scrap(self):
        """
        Fonction permettant de scrapper les données voulues, i.e. les données d'infoclimat concernant la température observée par différentes 
        stations météo entre 2011 et 2018

            Paramètres:
            ------------
                self.data_all : dict
                    Dictionnaire contenant toutes les données par années
        
            Output:
            ----------
                self.data_pop : dict
                    Dictionnaire contenant toutes les données par années actualisées
            
        """
        for y in self.data_all :
            for m in self.data_all[y] :
                url_temp = 'https://www.infoclimat.fr/stations-meteo/analyses-mensuelles.php?mois=' + str(m) + '&annee=' + str(y)
                raw_text = request.urlopen(url_temp).read()
                page = bs4.BeautifulSoup(raw_text,'lxml')
                tableau = page.find('table', {'id' : 'tableau-releves'})
                rows = tableau.find_all('tr')
        
                df = {
            'Villes' : [rows[i].find('a').text for i in range(1,len(rows))], #[rows[i].find_all('div')[0].text for i in range(1,len(rows))], #[rows[i].find('a').text for i in range(1,len(rows))],
            'Température minimale extrême du mois' : [rows[i].find('div').text for i in range(1,len(rows))],
            'Moyenne des températures minimales du mois' : [rows[i].find_all('td')[2].text for i in range(1,len(rows))],
            'Température moyenne du mois' : [rows[i].find_all('td')[3].text for i in range(1,len(rows))],
            'Moyenne des températures maximales du mois' : [rows[i].find_all('td')[4].text for i in range(1,len(rows))],
            'Température maximale extrême du mois' : [rows[i].find_all('td')[5].find('div').text for i in range(1,len(rows))],
            'Cumul de précipitation du mois' : [rows[i].find_all('td')[6].text for i in range(1,len(rows))],
            "Heure d'ensolleiment du mois" : [rows[i].find_all('td')[7].text for i in range(1,len(rows))],
            'Rafale maximale du mois' : [rows[i].find_all('td')[8].text for i in range(1,len(rows))] 
                    }
        
                self.data_all[y][m] = df

    def export(self):
        """
        Fonction intégrée d'export pour permettant de faciliter les manipulations.

        Paramètres:
        ------------
            self.data_pop : dict
                Dictionnaire contenant toutes les données par années
        
        Output:
        ----------
            Aucun
        """
        
        self.df_all = pandas.DataFrame(self.data_all)
        self.df_all.to_json('data_base.json')

    def rename(self):
        """
        Fonction intégrée permettant de renommer facilement les colonnes par le nom utilisé par infoclimat dans le but de faciliter le traitement.

        Paramètres :
        ------------
            self.df_all : DataFrame
                DataFrame contenant toutes les données météo extraites

        Output :
        --------
            self.df_all : DataFrame
                DataFrame contenant les mêmes données mais dont les colonnes ont été renommées
        """
        
        self.df_all = pandas.DataFrame(self.data_all)
        self.df_all.rename({'Villes' : 'ville', 
           'Température minimale extrême du mois' : 'tnn',
           'Moyenne des températures minimales du mois' : 'tnm', 
           'Température moyenne du mois' : 'tmm', 
           'Moyenne des températures maximales du mois' : 'txm', 
           'Température maximale extrême du mois' : 'txx', 
           'Cumul de précipitation du mois' : 'rr', 
           "Heure d'ensolleiment du mois" : 'ens', 
           'Rafale maximale du mois' : 'rafale'},axis=1,inplace = True)

class Population_departement :
    """
    Class permettant de scrapper et d'effectuer des opérations sur les données de l'INSEE concernant la population officielle des départements entre
    2011 et 2020.
    
    """
    def __init__ (self) :
        """
        Initialisation de la classe contenant :
            self.data_pop : Dictionnaire contenant les données
            self.urls : liste des urls nécessaire au scrapping
        """
        self.data_pop = {
            i : {} for i in range(2011,2021)
            }
        self.urls = [
            'https://www.insee.fr/fr/statistiques/2119745?sommaire=2119751',
            'https://www.insee.fr/fr/statistiques/2119678?sommaire=2119686',
            'https://www.insee.fr/fr/statistiques/2119468?sommaire=2119504',
            'https://www.insee.fr/fr/statistiques/2525762?sommaire=2525768',
            'https://www.insee.fr/fr/statistiques/3292643?sommaire=3292701',
            'https://www.insee.fr/fr/statistiques/3677771?sommaire=3677855',#
            'https://www.insee.fr/fr/statistiques/4265390?sommaire=4265511',
            'https://www.insee.fr/fr/statistiques/4989753?sommaire=4989761',
            'https://www.insee.fr/fr/statistiques/6013867?sommaire=6011075',
            'https://www.insee.fr/fr/statistiques/6683015?sommaire=6683037'
        ]

    def scrap(self):
        """ 
        Fonction permettant de scrapper les données voulues, i.e. la population officielle de chaque département de 2011 à 2020 depuis le site
        de l'INSEE.

            Paramètres:
            ------------
                self.data_pop : dict
                    Dictionnaire contenant toutes les données par années
        
            Output:
            ----------
                self.data_pop : dict
                    Dictionnaire contenant toutes les données par années actualisées
            
        """
        for i in range (len(self.urls)) :
            url = self.urls[i]
            raw_text = request.urlopen(url).read()
            page = bs4.BeautifulSoup(raw_text) #,'lxml')
            if i < 6 :
                fig = '1'
            else :
                fig = '2'
            tableau = page.find('table', {'id' : 'produit-tableau-figure' + fig})
            rows = tableau.find_all('tr')
            
            if 2011 + i < 2015 :
                self.data_pop[2011 + i] = {
                rows[j].text.split("\n")[1] : int(rows[j].text.split("\n")[3].replace('\xa0','').replace(' ','')) for j in range(3,len(rows))
                }
            elif 2011 + i == 2017 :
                self.data_pop[2011 + i] = {
                '0'+rows[j].text.split("\n")[1] : int(rows[j].text.split("\n")[3].replace('\xa0','').replace(' ','')) for j in range(1,10)
                }
                for j in range (10,len(rows)):
                    self.data_pop[2011 + i][rows[j].text.split("\n")[1]] = int(rows[j].text.split("\n")[3].replace('\xa0','').replace(' ',''))
            else :
                self.data_pop[2011 + i] = {
                    rows[j].text.split("\n")[1] : int(rows[j].text.split("\n")[3].replace('\xa0','').replace(' ','')) for j in range(1,len(rows))
                }
        

            
    def export(self) :
        """
        Fonction intégrée d'export pour permettant de faciliter les manipulations.

        Paramètres:
            ------------
                self.df_pop : DataFrame
                    Dictionnaire contenant toutes les données par années
        
            Output:
            ----------
                Aucun
        """
        self.df_pop = pandas.DataFrame(self.data_pop)
        self.df_pop.to_json('data_pop.json')

class Temperatures_dep :
    """
    Class permettant de traiter les données extraites et formalisées par la class 'Meteo'. 
    Elle permet notamment de déterminer sous forme de tableau :
        - les températures extrêmes par département et par années
        - les températures moyennes par département et par années
        - les températures extrêmes moyennes par département et par années
    """
    
    def __init__ (self) :
        """
        Initialisation de la classe contenant :
            self.data_raw : DataFrame contenant les données brutes extraites
            self.data_moy : DataFrame contenant les températures moyennes et extrêmes moyennes par département par années
            self.data_max : DataFrame contenant les températures maximales par départements et par années
            self.data_min : DataFrame contenant les températures minimales par départements et par années
        """
        self.data_raw = pd.read_csv('temperature-quotidienne-departementale.csv',sep=';')
        self.data_raw['key'] = self.data_raw['departement'] + self.data_raw['date_obs'].apply(lambda x : x[:4])
        
        self.data_moy = self.data_raw.groupby('key').mean('tmax')
        self.data_moy.rename({'tmin' : 'tmin_moy', 'tmax' : 'tmax_moy', 'tmoy' : 'tmoy_moy'},axis=1,inplace=True)
        
        self.data_max = self.data_raw.groupby('key').max('tmax')
        self.data_max.rename({'tmin' : 'tmin_max', 'tmax' : 'tmax_max', 'tmoy' : 'tmoy_max'},axis=1,inplace=True)
        
        self.data_min = self.data_raw.groupby('key').min('tmax')
        self.data_min.rename({'tmin' : 'tmin_min', 'tmax' : 'tmax_min', 'tmoy' : 'tmoy_min'},axis=1,inplace=True)
        
    def merge(self):
        """
        Fonction permettant de merge les différents dictionnaires initiaux sous la forme d'un dictionnaire complet.

        Paramètres :
        ------------
            self.data_moy : DataFrame
            self.data_max : DataFrame
            self.data_min : DataFrame

        Output :
        --------
            self.data_merged : DataFrame
                DF contenant toutes les données des tableaux initiaux sous la forme d'un unique tableau
        """
        self.data_merged = self.data_min.merge(self.data_moy,how='outer',on='key')
        self.data_merged = self.data_merged.merge(self.data_max,how='outer',on='key')
        return self.data_merged

    def export(self, table = 'merged'):
        """
        Fonction intégrée d'export pour permettant de faciliter les manipulations et sélectionner le tableau exporté.

        Paramètres:
            ------------
                self.data_raw : DataFrame
                self.data_moy : DataFrame
                self.data_max : DataFrame
                self.data_min : DataFrame
                table : string
                    paramètre permettant de choisir quelles tables exporter (par défaut seulement 'merged')
        
            Output:
            ----------
                Aucun
        """
        if table == 'all' :
            self.data_raw.to_csv('data_raw.csv')
            self.data_moy.to_csv('data_moy.csv')
            self.data_max.to_csv('data_max.csv')
            self.data_min.to_csv('data_min.csv')
            self.data_merged.to_csv('data_merged.csv')
            
        elif table == 'raw':
            self.data_raw.to_csv('data_raw.csv')

        elif table == 'merged' :
            self.data_merged.to_csv('data_merged.csv')