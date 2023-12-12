# Import des librairies 
import bs4
import lxml
import pandas as pd
import urllib
from urllib import request


# URL utiles 
url_soleil="https://static.data.gouv.fr/resources/donnees-du-temps-densoleillement-par-departements-en-france/20221207-142648/temp"
consumption_data_url_2018="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222018%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
consumption_data_url_2019="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222019%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
consumption_data_url_2020="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222020%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
consumption_data_url_2021="https://enedis.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-annuelle-residentielle-par-adresse/exports/csv?lang=fr&refine=annee%3A%222021%22&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

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
