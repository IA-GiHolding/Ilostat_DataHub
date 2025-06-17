import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


# ----------------------------
# CARGA DE DATOS ILOSTAT
# ----------------------------

url_fuerza_laboral = "https://rplumber.ilo.org/data/indicator/?id=POP_XWAP_SEX_AGE_NB_Q&lang=es&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=1983&timeto=2025&type=label&format=.tsv"

url_desempleo = "https://rplumber.ilo.org/data/indicator/?id=UNE_TUNE_SEX_AGE_NB_Q&lang=es&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=1983&timeto=2025&type=label&format=.tsv"

# Cargar archivos TSV
df_fuerza_laboral = pd.read_csv(url_fuerza_laboral, sep='\t')
df_desempleo = pd.read_csv(url_desempleo, sep='\t')

# Convertir coma decimal (.) en coma española (,)
df_fuerza_laboral['obs_value'] = df_fuerza_laboral['obs_value'].astype(str).str.replace('.', ',', regex=False)
df_desempleo['obs_value'] = df_desempleo['obs_value'].astype(str).str.replace('.', ',', regex=False)

# Convertir a numérico (si luego necesitas cálculos, vuelve a hacer to_numeric)
df_fuerza_laboral['obs_value'] = pd.to_numeric(df_fuerza_laboral['obs_value'].str.replace(',', '.'), errors='coerce')
df_desempleo['obs_value'] = pd.to_numeric(df_desempleo['obs_value'].str.replace(',', '.'), errors='coerce')

# Mapeo de géneros
genero_map = {'Hombres': 'H', 'Mujeres': 'M'}

# Función generalizada para obtener el último trimestre por año
def procesar_ilostat(df):
    df = df.dropna(subset=['obs_value']).copy()
    df['AÑO'] = df['time'].str.extract(r'(\d{4})')
    df['TRIM'] = df['time'].str.extract(r'Q([1-4])').astype(int)
    df['GENERO'] = df['sex.label'].map(genero_map)
    df['VALOR'] = df['obs_value']
    df['PAIS'] = df['ref_area.label'].str.strip()

    # Ordenar y quedarnos con el último trimestre por año
    df = df.sort_values(['PAIS', 'GENERO', 'AÑO', 'TRIM'])
    df = df.drop_duplicates(subset=['PAIS', 'GENERO', 'AÑO'], keep='last')

    return df[['PAIS', 'GENERO', 'AÑO', 'VALOR']]

# Aplicar a ambos datasets
df_fuerza_laboral_anual = procesar_ilostat(df_fuerza_laboral)
df_desempleo_anual = procesar_ilostat(df_desempleo)


print(df_fuerza_laboral_anual)
print(df_desempleo_anual)


# ----------------------------
# CARGA DE DATOS EUROSTAT
# ----------------------------

pais_map = {
    'Germany': 'Alemania', 'Austria': 'Austria', 'Bulgaria': 'Bulgaria', 'Belgium': 'Bélgica', 'Cyprus': 'Chipre',
    'Croatia': 'Croacia', 'Denmark': 'Dinamarca', 'Slovakia': 'Eslovaquia', 'Slovenia': 'Eslovenia',
    'Spain': 'España', 'Estonia': 'Estonia', 'Finland': 'Finlandia', 'France': 'Francia', 'Greece': 'Grecia',
    'Hungary': 'Hungría', 'Ireland': 'Irlanda', 'Italy': 'Italia', 'Latvia': 'Letonia', 'Lithuania': 'Lituania',
    'Luxembourg': 'Luxemburgo', 'Malta': 'Malta', 'Netherlands': 'Países Bajos', 'Poland': 'Polonia',
    'Portugal': 'Portugal', 'Czechia': 'Chequia', 'Romania': 'Rumanía', 'Sweden': 'Suecia'
}

url_males = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=M&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&c[TIME_PERIOD]=2024,2023,2022,2021,2020,2019,2018,2017,2016,2015&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"
url_females = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=F&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&c[TIME_PERIOD]=2024,2023,2022,2021,2020,2019,2018,2017,2016,2015&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"

df_pob_m = pd.read_csv(url_males)
df_pob_f = pd.read_csv(url_females)
df_poblacion = pd.concat([df_pob_m, df_pob_f], ignore_index=True)

df_poblacion['PAIS'] = df_poblacion['geo'].map(pais_map)
df_poblacion['GENERO'] = df_poblacion['sex'].map({'Males': 'H', 'Females': 'M'})
df_poblacion['AÑO'] = df_poblacion['TIME_PERIOD'].astype(str)
df_poblacion['VALOR'] = pd.to_numeric(df_poblacion['OBS_VALUE'], errors='coerce')
df_poblacion_limpio = df_poblacion[['PAIS', 'GENERO', 'AÑO', 'VALOR']].dropna()

print(df_poblacion_limpio)


# ----------------------------
# FILTROS STREAMLIT
# ----------------------------

st.set_page_config(layout="wide")

st.sidebar.header("Filtros")

años_pob = set(df_poblacion_limpio['AÑO'].unique())
años_fuerza = set(df_fuerza_laboral_anual['AÑO'].unique())
años_desemp = set(df_desempleo_anual['AÑO'].unique())

# Solo los años que están en las tres tablas
años_disponibles = sorted(list(años_pob & años_fuerza & años_desemp), reverse=True)
año = st.sidebar.selectbox("Selecciona el año", años_disponibles)

genero_opcion = st.sidebar.selectbox("Selecciona género", options=['Todos', 'H', 'M'])
generos = ['H', 'M'] if genero_opcion == 'Todos' else [genero_opcion]

# Leyenda visual
st.sidebar.markdown("### Leyenda")
st.sidebar.markdown("""
<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 2px;'>
    <div style='width: 12px; height: 12px; background-color: #00145A;'></div>
    <span>UE</span>
</div>
<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 2px;'>
    <div style='width: 12px; height: 12px; background-color: #f30000;'></div>
    <span>Iberia</span>
</div>
<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 2px;'>
    <div style='width: 12px; height: 12px; background-color: #1D57FB;'></div>
    <span>España</span>
</div>
<div style='display: flex; align-items: center; gap: 8px;'>
    <div style='width: 12px; height: 12px; background-color: #C6D9DA;'></div>
    <span>Portugal</span>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# CÁLCULOS
# ----------------------------

df_pob_filtro = df_poblacion_limpio[(df_poblacion_limpio['AÑO'] == año) & (df_poblacion_limpio['GENERO'].isin(generos))]
df_fuerza_filtro = df_fuerza_laboral_anual[(df_fuerza_laboral_anual['AÑO'] == año) & (df_fuerza_laboral_anual['GENERO'].isin(generos))]
df_desemp_filtro = df_desempleo_anual[(df_desempleo_anual['AÑO'] == año) & (df_desempleo_anual['GENERO'].isin(generos))]

poblacion_ue = df_pob_filtro['VALOR'].sum()
poblacion_iberia = df_pob_filtro[df_pob_filtro['PAIS'].isin(['España', 'Portugal'])]['VALOR'].sum()
poblacion_espana = df_pob_filtro[df_pob_filtro['PAIS'].isin(['España'])]['VALOR'].sum()
poblacion_portugal = df_pob_filtro[df_pob_filtro['PAIS'].isin(['Portugal'])]['VALOR'].sum()

fuerza_ue = df_fuerza_filtro['VALOR'].sum()
fuerza_iberia = df_fuerza_filtro[df_fuerza_filtro['PAIS'].isin(['España', 'Portugal'])]['VALOR'].sum()
fuerza_espana = df_fuerza_filtro[df_fuerza_filtro['PAIS'] == 'España']['VALOR'].sum()
fuerza_portugal = df_fuerza_filtro[df_fuerza_filtro['PAIS'] == 'Portugal']['VALOR'].sum()

desemp_ue = df_desemp_filtro['VALOR'].sum()
desemp_iberia = df_desemp_filtro[df_desemp_filtro['PAIS'].isin(['España', 'Portugal'])]['VALOR'].sum()
desemp_espana = df_desemp_filtro[df_desemp_filtro['PAIS'] == 'España']['VALOR'].sum()
desemp_portugal = df_desemp_filtro[df_desemp_filtro['PAIS'] == 'Portugal']['VALOR'].sum()

porc_espana = (poblacion_espana / poblacion_ue) * 100 if poblacion_ue else 0
porc_portugal = (poblacion_espana / poblacion_ue) * 100 if poblacion_ue else 0
porc_iberia = (poblacion_iberia / poblacion_ue) * 100 if poblacion_ue else 0
porc_resto = 100 - porc_iberia
porc_fuerza_iberia = (fuerza_iberia / poblacion_iberia) * 100 if poblacion_iberia else 0
porc_fuerza_ue = (fuerza_ue / poblacion_ue) * 100 if poblacion_ue else 0
porc_desemp_iberia = (desemp_iberia / poblacion_iberia) * 100 if poblacion_iberia else 0
porc_desemp_ue = (desemp_ue / poblacion_ue) * 100 if poblacion_ue else 0

# ----------------------------
# VISUALIZACIÓN
# ----------------------------

col1, col2, col3 = st.columns([1, 1, 1])

# Población
with col1:
    st.markdown("""
        <div style='text-align: center;'>
            <h3>Población</h3>
            <h5>% Iberia vs UE</h5>
            <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; margin-left:-20px;'>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #f30000;'></div>
                    <span>Iberia {0:.2f}%</span>
                </div>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #00145A;'></div>
                    <span>UE {1:.2f}%</span>
                </div>
            </div>
        </div>
    """.format(porc_iberia, porc_resto), unsafe_allow_html=True)



    # Datos para el gráfico
    labels = ['Iberia', 'UE']
    values = [porc_iberia, porc_resto]
    colors = ['#f30000', '#00145A']

    # Crear gráfico tipo dona con Plotly
    fig1 = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont=dict(color='white', size=15),
        hovertemplate='<b>%{label}</b><br>%{value:.2f}%<extra></extra>'
    )])

    # Layout limpio
    fig1.update_layout(
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=150),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    # Configuración sin botones
    config_plotly = {
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "zoom2d", "pan2d", "select2d", "lasso2d",
            "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian", "toImage"
        ]
    }

    # Mostrar en Streamlit
    st.plotly_chart(fig1, use_container_width=True, config=config_plotly)
    

# Fuerza Laboral
with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <h3>Fuerza Laboral</h3>
            <h5>% Iberia vs Población UE</h5>
            <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;margin-left:-20px;'>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #f30000;'></div>
                    <span>Iberia {0:.2f}%</span>
                </div>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #00145A;'></div>
                    <span>UE {1:.2f}%</span>
                </div>
            </div>
        </div>
    """.format(porc_fuerza_iberia, porc_fuerza_ue), unsafe_allow_html=True)
    

    df_barras_plotly = pd.DataFrame({
        'PAIS': ['Portugal', 'España', 'UE'],
        'VALOR': [fuerza_portugal, fuerza_espana, fuerza_ue]
    })




    df_barras_plotly = df_barras_plotly.sort_values(by='VALOR', ascending=False)

    fig2 = px.bar(
        df_barras_plotly,
        x='VALOR',
        y='PAIS',
        orientation='h',
        text='VALOR',
        color='PAIS',
        color_discrete_map={
            'UE': '#00145A',
            'España': '#1D57FB',
            'Portugal': '#C6D9DA'
        }
    )

    fig2.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Valor: %{x:,.0f}<extra></extra>',
        cliponaxis=False,  # 👈 asegura que el texto no se recorte
        marker=dict(line=dict(width=0)),  # opcional para un borde más limpio
    )

    fig2.update_layout(
        dragmode=False,
        bargap=0.15,  # 👈 separa las barras para hacerlas más finas
        xaxis_showticklabels=False,
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=150)  # 👈 aumenta margen derecho
    )

    config_plotly = {
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "zoom2d", "pan2d", "select2d", "lasso2d",
            "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian", "toImage"
        ]
    }

    st.plotly_chart(fig2, use_container_width=True, config=config_plotly)


# Desempleo
with col3:
    st.markdown("""
        <div style='text-align: center;'>
            <h3>Desempleo</h3>
            <h5>% Iberia vs Población UE</h5>
            <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;margin-left:-20px;'>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #f30000;'></div>
                    <span>Iberia {0:.2f}%</span>
                </div>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #00145A;'></div>
                    <span>UE {1:.2f}%</span>
                </div>
            </div>
        </div>
    """.format(porc_desemp_iberia, porc_desemp_ue), unsafe_allow_html=True)

    df_barras_plotly3 = pd.DataFrame({
    'PAIS': ['Portugal', 'España', 'UE'],
    'VALOR': [desemp_portugal, desemp_espana, desemp_ue]
    })
   
    df_barras_plotly3 = df_barras_plotly3.sort_values(by='VALOR', ascending=False)

    # Gráfico Plotly para Desempleo
    fig3 = px.bar(
        df_barras_plotly3,
        x='VALOR',
        y='PAIS',
        orientation='h',
        text='VALOR',
        color='PAIS',
        color_discrete_map={
            'UE': '#00145A',
            'España': '#1D57FB',
            'Portugal': '#C6D9DA'
        }
    )

    # Personalización de barras
    fig3.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Valor: %{x:,.0f}<extra></extra>',
        cliponaxis=False,
        marker=dict(line=dict(width=0))
    )

    # Estilo del gráfico
    fig3.update_layout(
        dragmode=False,
        bargap=0.15,
        xaxis_showticklabels=False,
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=150)
    )

    # Configuración Plotly para ocultar botones
    config_plotly = {
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "zoom2d", "pan2d", "select2d", "lasso2d",
            "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian", "toImage"
        ]
    }

    # Renderizado en Streamlit
    st.plotly_chart(fig3, use_container_width=True, config=config_plotly)

st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    
# Última actualización: Mon Jun 16 14:32:52 UTC 2025
# Última actualización: Mon Jun 16 14:50:47 UTC 2025
# Última actualización: Mon Jun 16 15:38:57 UTC 2025
# Última actualización: Tue Jun 17 07:40:34 UTC 2025
# Última actualización: Tue Jun 17 07:53:27 UTC 2025
# Última actualización: Tue Jun 17 09:13:15 UTC 2025
