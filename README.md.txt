# Ilostat Dashboard  

Este proyecto permite visualizar indicadores de la base de datos de Ilostat (OIT) de forma dinámica con Streamlit y Plotly.  




## Indicadores 

 

Población (Download, JSON, Only displayed dimensions, Copy API Link) 

url_males = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=M&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"
url_females = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=F&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"

url_fuerza_laboral = "https://rplumber.ilo.org/data/indicator/?id=POP_XWAP_SEX_AGE_NB_Q&lang=es&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=2019&type=label&format=.xlsx"
url_desempleo = "https://rplumber.ilo.org/data/indicator/?id=UNE_TUNE_SEX_AGE_NB_Q&lang=es&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=2019&type=label&format=.xlsx"





# Para actualizar algún cambio en el código en Git Hub, introducir estos comandos en la terminal


git status
git pull origin main --rebase
git add .
git commit -m "Ultimos retoques"
git push origin main





# SDG indicator 8.5.2. - Unemployment rate by disability status (%) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=SDG_0852_SEX_DSB_RT_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=SDG_0852_SEX_DSB_RT_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023&type=label&format=.tsv


# Working-age population by sex, disability status and labour market status (thousands) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=POP_XWAP_SEX_DSB_LMS_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&classif2=LMS_STATUS_EMP+LMS_STATUS_UNE+LMS_STATUS_EIP&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=POP_XWAP_SEX_DSB_LMS_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&classif2=LMS_STATUS_EMP+LMS_STATUS_UNE+LMS_STATUS_EIP&timefrom=2004&timeto=2023&type=label&format=.tsv


# Labour force by sex and disability status (thousands) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=EAP_TEAP_SEX_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=EAP_TEAP_SEX_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023&type=label&format=.tsv


# Employment by sex, economic activity and disability status (thousands) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=EMP_TEMP_SEX_ECO_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=ECO_SECTOR_AGR+ECO_SECTOR_NAG+ECO_SECTOR_IND+ECO_SECTOR_SER+ECO_SECTOR_X+ECO_AGGREGATE_TOTAL+ECO_AGGREGATE_AGR+ECO_AGGREGATE_MAN+ECO_AGGREGATE_CON+ECO_AGGREGATE_MKT+ECO_AGGREGATE_PUB+ECO_AGGREGATE_X&classif2=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=EMP_TEMP_SEX_ECO_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=ECO_SECTOR_AGR+ECO_SECTOR_NAG+ECO_SECTOR_IND+ECO_SECTOR_SER+ECO_SECTOR_X+ECO_AGGREGATE_TOTAL+ECO_AGGREGATE_AGR+ECO_AGGREGATE_MAN+ECO_AGGREGATE_CON+ECO_AGGREGATE_MKT+ECO_AGGREGATE_PUB+ECO_AGGREGATE_X&classif2=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023&type=label&format=.tsv


# Employment by sex, occupation and disability status (thousands) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=EMP_TEMP_SEX_OCU_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=OCU_SKILL_L3-4+OCU_SKILL_L2+OCU_SKILL_L1+OCU_SKILL_X&classif2=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=EMP_TEMP_SEX_OCU_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=OCU_SKILL_L3-4+OCU_SKILL_L2+OCU_SKILL_L1+OCU_SKILL_X&classif2=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023&type=label&format=.tsv


# Employment-topopulation ratio by sex and disability status (%) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=EMP_DWAP_SEX_DSB_RT_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=EMP_DWAP_SEX_DSB_RT_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023&type=label&format=.tsv


# Unemployment by sex and disability status (thousands) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=UNE_TUNE_SEX_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=UNE_TUNE_SEX_DSB_NB_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023&type=label&format=.tsv


# Inactivity rate by sex and disability status (%) - Annual:

https://rplumber.ilo.org/dataexplorer/?id=EIP_DWAP_SEX_DSB_RT_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023
https://rplumber.ilo.org/data/indicator/?id=EIP_DWAP_SEX_DSB_RT_A&ref_area=ESP&sex=SEX_M+SEX_F&classif1=DSB_STATUS_DIS+DSB_STATUS_NODIS&timefrom=2004&timeto=2023&type=label&format=.tsv
