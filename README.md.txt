# Ilostat Dashboard  

Este proyecto permite visualizar indicadores de la base de datos de Ilostat (OIT) de forma dinámica con Streamlit y Plotly.  




## Indicadores 

 

Población (Download, CSV, Only displayed dimensions, No seleccionar ninguna casilla, Copy API Link)

url_males = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=M&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"
url_females = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=F&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"


FL y DE (27 países, H y M, total de edad, exportar CSV, copiar enlace)

df_fuerza_laboral = pd.read_csv("https://rplumber.ilo.org/data/indicator/?id=POP_XWAP_SEX_AGE_NB_Q&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=2019&format=.csv")
df_desempleo = pd.read_csv("https://rplumber.ilo.org/data/indicator/?id=UNE_TUNE_SEX_AGE_NB_Q&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=2019&format=.csv")





# Para actualizar algún cambio en el código en Git Hub, introducir estos comandos en la terminal


git status
git pull origin main --rebase
git add .
git commit -m "Ultimos retoques"
git push origin main



_________________OPCIÓN MANUAL____________________

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


# ----------------------------
# CARGA DE DATOS ILOSTAT
# ----------------------------

ruta_fuerza_laboral = "data/POP_XWAP_SEX_AGE_NB_Q-20250624T1317.xlsx"
ruta_desempleo = "data/UNE_TUNE_SEX_AGE_NB_Q-20250624T1317.xlsx"

df_fuerza_laboral = pd.read_excel(ruta_fuerza_laboral, engine="openpyxl")
df_desempleo = pd.read_excel(ruta_desempleo, engine="openpyxl")

# Convertir valores a numérico y multiplicar por mil (porque están en miles)
df_fuerza_laboral['obs_value'] = pd.to_numeric(
    df_fuerza_laboral['obs_value'].astype(str).str.replace(',', '.'), errors='coerce'
) * 1000

df_desempleo['obs_value'] = pd.to_numeric(
    df_desempleo['obs_value'].astype(str).str.replace(',', '.'), errors='coerce'
) * 1000

# Mapeo de géneros
genero_map = {'Hombres': 'H', 'Mujeres': 'M'}

# Función para procesar los datos y quedarse con el último trimestre por año
def procesar_ilostat(df):
    df = df.dropna(subset=['obs_value']).copy()
    df['AÑO'] = df['time'].str.extract(r'(\d{4})')
    df['TRIM'] = df['time'].str.extract(r'Q([1-4])').astype(int)
    df['GENERO'] = df['sex.label'].map(genero_map)
    df['VALOR'] = df['obs_value']
    df['PAIS'] = df['ref_area.label'].str.strip()

    # Ordenar y filtrar el último trimestre por año
    df = df.sort_values(['PAIS', 'GENERO', 'AÑO', 'TRIM'])
    df = df.drop_duplicates(subset=['PAIS', 'GENERO', 'AÑO'], keep='last')

    return df[['PAIS', 'GENERO', 'AÑO', 'VALOR']]

# Aplicar función a los datasets
df_fuerza_laboral_anual = procesar_ilostat(df_fuerza_laboral)
df_desempleo_anual = procesar_ilostat(df_desempleo)

# Mostrar resultados
print(df_fuerza_laboral_anual)
print(df_desempleo_anual)
