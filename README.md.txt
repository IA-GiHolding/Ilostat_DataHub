# Ilostat Dashboard  

Este proyecto permite visualizar indicadores de la base de datos de Ilostat (OIT) de forma dinámica con Streamlit y Plotly.  


## Indicadores 

 

Población (Download, JSON, Only displayed dimensions, Copy API Link) 

MALES: https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=M&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&c[TIME_PERIOD]=2024,2023,2022,2021,2020,2019,2018,2017,2016,2015&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only  

FEMALES: https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=F&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&c[TIME_PERIOD]=2024,2023,2022,2021,2020,2019,2018,2017,2016,2015&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only 

Fuerza laboral (27 países, H y M, total de edad, exportar TSV, copiar enlace) 

https://rplumber.ilo.org/data/indicator/?id=POP_XWAP_SEX_AGE_NB_Q&lang=es&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=1983&timeto=2025&type=label&format=.tsv 

Desempleo 

https://rplumber.ilo.org/data/indicator/?id=UNE_TUNE_SEX_AGE_NB_Q&lang=es&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=1983&timeto=2025&type=label&format=.tsv 





## Tecnologías 

 
- Python 
- Streamlit 
- Pandas 
- Plotly 

## Uso 

1. Clona este repositorio 
2. Instala dependencias con `pip install -r requirements.txt` 
3. Ejecuta `streamlit run app.py` 


# Para actualizar manualmente los datos, introducir estos comandos en la terminal

git init
git add .
git commit -m "Nuevo cambio"
git push origin main