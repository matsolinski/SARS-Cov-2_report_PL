# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 21:10:52 2020

@author: Mateusz Soliński
"""

## Import Libraries
import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
#%matplotlib inline
#pip install SomePackage
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
plt.rcParams['figure.figsize'] = [15, 5]
from IPython import display
from ipywidgets import interact, widgets
from datetime import datetime
import xlrd
# CURRENT AND YESTERDAY DATE AND TIME
now = datetime.now()
date_time_trailer = now.strftime("%Y_%m_%d")

# DEFINES COUNTRY NAMES FIXES DICTIONARY
countries_fixes_dict_CSSE = {'West Bank and Gaza': 'Palestine'}
                        
## Read Data for Cases, Deaths and Recoveries
# ConfirmedCases_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
# Deaths_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
#Recoveries_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

#WCZYTYWANIE TYLKO DANYCH Z OSTATNIEGO DNIA

ConfirmedCases_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
Deaths_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
Recoveries_raw=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

#zamiana nazw krajow
ConfirmedCases_raw['Country/Region'] = ConfirmedCases_raw['Country/Region'].replace({'West Bank and Gaza': 'Palestine'})
Deaths_raw['Country/Region'] = Deaths_raw['Country/Region'].replace({'West Bank and Gaza': 'Palestine'})
Recoveries_raw['Country/Region'] = Recoveries_raw['Country/Region'].replace({'West Bank and Gaza': 'Palestine'})


##### TU JEST SEKCJA LACZENIA Z WORLDOMETER - BYC MOZE JESZCZE BEDZIE POTRZEBNA....

##dodawanie wczorajszego recovery z worldometer
#Recoveries_raw = pd.merge(Recoveries_raw, worldometer_recovered_DF, left_on='Country/Region', right_on='Country/Region', how='inner')

# Recoveries_raw_last_day = Recoveries_raw.iloc[:,-1]
# Deaths_raw_last_day = Recoveries_raw.iloc[:,-1]
# ConfirmedCases_raw_last_day = Recoveries_raw.iloc[:,-1]
    
#######wyznaczanie branie ostatniej kolumny
# Recoveries_raw = pd.read_excel (r'Recoveries_raw_backup.xlsx')
# Deaths_raw = pd.read_excel (r'Deaths_raw_backup.xlsx')
# ConfirmedCases_raw = pd.read_excel (r'ConfirmedCases_raw_backup.xlsx')

# Recoveries_raw.to_excel(r'./Recoveries_raw_backup.xlsx', index = True)
# Deaths_raw.to_excel(r'./Deaths_raw_backup.xlsx', index = True)
# ConfirmedCases_raw.to_excel(r'./ConfirmedCases_raw_backup.xlsx', index = True)

# Recoveries_raw.to_excel(r'./backup_data/Recoveries_raw_backup' + date_time_trailer +  '.xlsx', index = True)
# Deaths_raw.to_excel(r'./backup_data/Deaths_raw_backup' + date_time_trailer +  '.xlsx', index = True)
# ConfirmedCases_raw.to_excel(r'./backup_data/ConfirmedCases_raw_backup' + date_time_trailer + '.xlsx', index = True)

######################################################################################
Recoveries_raw.to_excel(r'./backup_data/Recoveries_raw_backup' + date_time_trailer +  '.xlsx', index = True)
Deaths_raw.to_excel(r'./backup_data/Deaths_raw_backup' + date_time_trailer +  '.xlsx', index = True)
ConfirmedCases_raw.to_excel(r'./backup_data/ConfirmedCases_raw_backup' + date_time_trailer + '.xlsx', index = True)



#funkcja, ktora zamienia uklad tabeli do takiego, gdzie daty sa w kolejnych wierszach a nie w kolumnach
def cleandata(df_raw):
    df_cleaned=df_raw.melt(id_vars=['Province/State','Country/Region','Lat','Long'],value_name='Cases',var_name='Date')
    #df_cleaned=df_cleaned.set_index(['Country/Region','Province/State','Date'])
    return df_cleaned 

     

# Clean all datasets
ConfirmedCases=cleandata(ConfirmedCases_raw)
Deaths=cleandata(Deaths_raw)
Recoveries=cleandata(Recoveries_raw)

# list(ConfirmedCases.index.get_level_values(0))
# list(ConfirmedCases.index.get_level_values(1))

# #sumowanie przypadkow pod prowincjach (wyswietlam tylko kraje)
ConfirmedCases = ConfirmedCases.groupby(['Country/Region','Date']).sum()
ConfirmedCases["Date"] = list(ConfirmedCases.index.get_level_values(1))
ConfirmedCases["Country/Region"] = list(ConfirmedCases.index.get_level_values(0))
Deaths = Deaths.groupby(['Country/Region','Date']).sum()
Recoveries = Recoveries.groupby(['Country/Region','Date']).sum()

ConfirmedCases.index.names = ['Country/Region inx','Date inx']
   #DataFrame ze wszystkimi danymi do eksportu
df_final = pd.DataFrame({
        # "Province/State": ConfirmedCases['Province/State'],
        "Country/Region": ConfirmedCases['Country/Region'],
        "Lat": ConfirmedCases['Lat'],
        "Long": ConfirmedCases['Long'],
        "Date": ConfirmedCases['Date'],
        "Confirmed": ConfirmedCases['Cases'],
        "Deaths": Deaths['Cases'],
        "Recoveries": Recoveries['Cases'],
        "OrderNumber_Confirmed":np.zeros(len(ConfirmedCases)),
        "OrderNumber_Deaths":np.zeros(len(ConfirmedCases))
        })
#df_final2 = df_final.sort_values(['Date'])


    #if Country_unique_Confirmed.index(i):
        #res_list.extend([i]) 

#    #DataFrame ze wszystkimi danymi do eksportu
# df_final_recovered = pd.DataFrame({
#         #"Province/State": Recoveries['Province/State'],
#         "Country/Region": Recoveries['Country/Region'],
#         #"Lat": Recoveries['Lat'],
#        # "Long": Recoveries['Long'],
#         "Date": Recoveries['Date'],
#         #"Confirmed": ConfirmedCases['Cases'],
#         #"Deaths": Deaths['Cases'],
#         "Recoveries": Recoveries['Cases']
#         #"OrderNumber_Confirmed":np.zeros(len(ConfirmedCases)),
#         #"OrderNumber_Deaths":np.zeros(len(ConfirmedCases))
#         })

Country_unique = list(np.unique(df_final['Country/Region']))
#convert date
df_final['Date'] = [datetime.strptime(df_final['Date'][i], '%m/%d/%y') for i in range(0,len(df_final)) ]
df_final = df_final.sort_values(['Country/Region','Date'])

# df_final_recovered['Date'] = [datetime.datetime.strptime(df_final_recovered['Date'][i], '%m/%d/%Y') for i in range(0,len(df_final_recovered)) ]
# df_final_recovered = df_final_recovered.sort_values(['Country/Region','Date'])

 #nadanie numeru porzadkowego dla kazdego kraju od dnia stwierdzenia 150 przypadków w danym kraju
for j in range(0,len(Country_unique)):
     
    countryTemp = Country_unique[j]  
   # list_temp = list(df_final['Country/Region'])
    res_list = [] #lista indeksow w DataFrame df_final, w ktorych wystepuje dany kraj
    for i in range(0,len(df_final)):
        if df_final['Country/Region'][i] == countryTemp:
           res_list.extend([i]) 
    #res_list = [i for i, value in enumerate(list_temp) if value == countryTemp] 
    
    ind = 0
    
    current_date = df_final["Date"][res_list[0]]
    
    df_final_temp_confirmed = df_final["Confirmed"][res_list] #wyniki tylko dla danego kraju i jego prowincji
    df_final_temp_date = df_final["Date"][res_list] #wyniki tylko dla danego kraju i jego prowincji
    ind_minus_prepare = 0
    howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])
    for k in range(0,len(res_list)):
            
        #policz ile bylo przypadkow danego dnia w kraju we wszystkich jego prowincjach/stanach (dotyczy glownie US i Chin)
        
       
        if howManyCasesInCurrentDay<150:
            # print(current_date)
            #df_final["OrderNumber"][res_list[k]]=ind_minus
            if current_date != df_final["Date"][res_list[k]]:
                current_date = df_final["Date"][res_list[k]] #zamiana current date
                
                ind_minus_prepare = ind_minus_prepare + 1 #policzenie ile bylo dni z mniej niz 150 przypadkami, co jest konieczne do przypisania ujemnych dni od dnia 0 (osiągnienie 150 przypadkow) kilka linijek nizej
        else:        
            if current_date != df_final["Date"][res_list[k]]:
                current_date = df_final["Date"][res_list[k]] #zamiana current date
                ind = ind + 1
            df_final["OrderNumber_Confirmed"][res_list[k]]=ind #przypisanie dnia od dnia 0 (150 przypadkow)    
        howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])    
 
    ind_minus2 = 0-ind_minus_prepare #indykator ujemnych dni od dnia zero (150 przypadkow)
    current_date = df_final["Date"][res_list[0]]
    for k in range(0,len(res_list)):
        
        howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])
        if howManyCasesInCurrentDay<150:           
            if current_date != df_final["Date"][res_list[k]]:
                current_date = df_final["Date"][res_list[k]] #zamiana current date
                ind_minus2 = ind_minus2 + 1
            df_final["OrderNumber_Confirmed"][res_list[k]]=ind_minus2 #przypisanie ujemnego dnia od dnia 0 (150 przypadkow)   

 #proba nadania numeru porzadkowego dla kazdego kraju od dnia sstwierdzenia przynajmniej 5 zgonow  
for j in range(0,len(Country_unique)):
  # j=52
    countryTemp = Country_unique[j]  
    res_list = [] #lista indeksow w DataFrame df_final, w ktorych wystepuje dany kraj
    for i in range(0,len(df_final)):
        if df_final['Country/Region'][i] == countryTemp:
           res_list.extend([i]) 
    
    ind = 0
    
    current_date = df_final["Date"][res_list[0]]
    
    df_final_temp_confirmed = df_final["Deaths"][res_list] #wyniki tylko dla danego kraju i jego prowincji
    df_final_temp_date = df_final["Date"][res_list] #wyniki tylko dla danego kraju i jego prowincji
    ind_minus_prepare = 0
    howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])
    for k in range(0,len(res_list)):
            
        #policz ile bylo przypadkow danego dnia w kraju we wszystkich jego prowincjach (dotyczy glownie US i Chin)
        
        
        if howManyCasesInCurrentDay<5:
            #df_final["OrderNumber"][res_list[k]]=ind_minus
            if current_date != df_final["Date"][res_list[k]]:
                current_date = df_final["Date"][res_list[k]] #current date
                
                ind_minus_prepare = ind_minus_prepare + 1
        else:       
            if current_date != df_final["Date"][res_list[k]]:
                current_date = df_final["Date"][res_list[k]] #current date
                ind = ind + 1
            df_final["OrderNumber_Deaths"][res_list[k]]=ind    
        howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])    
 
    ind_minus2 = 0-ind_minus_prepare
    current_date = df_final["Date"][res_list[0]]
    howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])
    for k in range(0,len(res_list)):
        
        howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])
        if howManyCasesInCurrentDay<5:
            if current_date != df_final["Date"][res_list[k]]:
                current_date = df_final["Date"][res_list[k]] #current date
                ind_minus2 = ind_minus2 + 1                
            df_final["OrderNumber_Deaths"][res_list[k]]=ind_minus2    
       # howManyCasesInCurrentDay = sum(df_final_temp_confirmed[df_final_temp_date == current_date])
    
    # print(df_final["OrderNumber_Deaths"][res_list])
    # print(df_final["Deaths"][res_list])
                #export
#df_final.to_excel(r'AllData_20032020_order1.xlsx', index = False)
df_final.to_excel(r'AllData_order.xlsx', index = False)
# df_final_recovered.to_excel(r'AllData_recovered.xlsx', index = False)

#ConfirmedCases.to_excel(r'ConfirmedCases.xlsx', index = False)
#Deaths.to_excel(r'Deaths.xlsx', index = False)
#Recoveries.to_excel(r'Recoveries.xlsx', index = False)
