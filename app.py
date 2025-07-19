import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


#-----------------------------------
# CARGA DE DATOS DE ILOSTAT
#-----------------------------------

# Cargar CSVs desde ILOSTAT en español (labels ya aplicados)
df_fuerza_laboral = pd.read_csv("https://rplumber.ilo.org/data/indicator/?id=POP_XWAP_SEX_AGE_NB_Q&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=2019&format=.csv&type=label&lang=es")
df_desempleo = pd.read_csv("https://rplumber.ilo.org/data/indicator/?id=UNE_TUNE_SEX_AGE_NB_Q&ref_area=DEU+AUT+BGR+BEL+CYP+HRV+DNK+SVK+SVN+ESP+EST+FIN+FRA+GRC+HUN+IRL+ITA+LVA+LTU+LUX+MLT+NLD+POL+PRT+CZE+ROU+SWE&sex=SEX_M+SEX_F&classif1=AGE_AGGREGATE_TOTAL&timefrom=2019&format=.csv&type=label&lang=es")

print(df_desempleo.columns)

# Convertir a numérico y multiplicar por mil
df_fuerza_laboral['obs_value'] = pd.to_numeric(
    df_fuerza_laboral['obs_value'].astype(str).str.replace(',', '.'), errors='coerce'
) * 1000

df_desempleo['obs_value'] = pd.to_numeric(
    df_desempleo['obs_value'].astype(str).str.replace(',', '.'), errors='coerce'
) * 1000

# Función generalizada para obtener el último trimestre por año
def procesar_ilostat(df):
    df = df.dropna(subset=['obs_value']).copy()
    df['AÑO'] = df['time'].str.extract(r'(\d{4})')
    df['TRIM'] = df['time'].str.extract(r'Q([1-4])').astype(int)
    df['GENERO'] = df['sex.label']  # Ya viene en español
    df['VALOR'] = df['obs_value']
    df['PAIS'] = df['ref_area.label']  # Ya viene en español

    # Ordenar y quedarnos con el último trimestre por año, por país y género
    df = df.sort_values(['PAIS', 'GENERO', 'AÑO', 'TRIM'])
    df = df.drop_duplicates(subset=['PAIS', 'GENERO', 'AÑO'], keep='last')

    return df[['PAIS', 'GENERO', 'AÑO', 'VALOR']]

# Aplicar a ambos datasets
df_fuerza_laboral_anual = procesar_ilostat(df_fuerza_laboral)
df_desempleo_anual = procesar_ilostat(df_desempleo)

# Mostrar resultados
print(df_fuerza_laboral_anual)
print(df_desempleo_anual)

# ----------------------------
# CARGA DE DATOS EUROSTAT
# ----------------------------

# Mapeo de nombres de países en inglés → español
pais_map = {
    'Germany': 'Alemania',
    'Austria': 'Austria',
    'Bulgaria': 'Bulgaria',
    'Belgium': 'Bélgica',
    'Cyprus': 'Chipre',
    'Croatia': 'Croacia',
    'Denmark': 'Dinamarca',
    'Slovakia': 'Eslovaquia',
    'Slovenia': 'Eslovenia',
    'Spain': 'España',
    'Estonia': 'Estonia',
    'Finland': 'Finlandia',
    'France': 'Francia',
    'Greece': 'Grecia',
    'Hungary': 'Hungría',
    'Ireland': 'Irlanda',
    'Italy': 'Italia',
    'Latvia': 'Letonia',
    'Lithuania': 'Lituania',
    'Luxembourg': 'Luxemburgo',
    'Malta': 'Malta',
    'Netherlands': 'Países Bajos',
    'Poland': 'Polonia',
    'Portugal': 'Portugal',
    'Czechia': 'Chequia',
    'Romania': 'Rumanía',
    'Sweden': 'Suecia'
}


# URLs Eurostat (los datos vienen en inglés)
url_males = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=M&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"
url_females = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/3.0/data/dataflow/ESTAT/demo_pjan/1.0/*.*.*.*.*?c[freq]=A&c[unit]=NR&c[age]=TOTAL&c[sex]=F&c[geo]=BE,BG,CZ,DK,DE,EE,IE,EL,ES,FR,HR,IT,CY,LV,LT,LU,MT,NL,HU,AT,PL,PT,RO,SI,SK,FI,SE&compress=false&format=csvdata&formatVersion=1.0&lang=en&labels=label_only"

# Cargar datos
df_pob_m = pd.read_csv(url_males)
df_pob_f = pd.read_csv(url_females)
df_poblacion = pd.concat([df_pob_m, df_pob_f], ignore_index=True)

print (df_poblacion["geo"])

# Mapear género a 'Hombres' y 'Mujeres'
df_poblacion['GENERO'] = df_poblacion['sex'].map({'Males': 'Hombres', 'Females': 'Mujeres'})

# Mapear país a su nombre en español
df_poblacion['PAIS'] = df_poblacion['geo'].map(pais_map)

# Extraer año y valor
df_poblacion['AÑO'] = df_poblacion['TIME_PERIOD'].astype(str)
df_poblacion['VALOR'] = pd.to_numeric(df_poblacion['OBS_VALUE'], errors='coerce')

# Dataset limpio
df_poblacion_limpio = df_poblacion[['PAIS', 'GENERO', 'AÑO', 'VALOR']].dropna()

# Mostrar resultados
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

# Opciones de género ya con nombres completos
genero_opcion = st.sidebar.selectbox("Selecciona el género", options=['Todos', 'Hombres', 'Mujeres'])
generos = ['Hombres', 'Mujeres'] if genero_opcion == 'Todos' else [genero_opcion]

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
poblacion_resto = poblacion_ue-poblacion_iberia

# Calcular valores y añadir versión formateada para el hover
values = [poblacion_iberia, poblacion_resto]
customdata = [f"{int(val):,}".replace(",", ".") for val in values]

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
            <p style="font-size: 35px; font-weight: bold; margin-bottom: 1px;">Población</p>
            <p style="font-size: 20px; font-weight: light;">% Iberia vs UE</p>
            <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;'>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #f30000;'></div>
                    <span>Iberia {0:.0f}%</span>
                </div>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #00145A;'></div>
                    <span>UE {1:.0f}%</span>
                </div>
            </div>
        </div>
    """.format(porc_iberia, porc_resto), unsafe_allow_html=True)

    # ► NUEVO: usa valores absolutos para el tamaño de las porciones
    poblacion_resto = poblacion_ue - poblacion_iberia   # resto de la UE
    labels  = ['Iberia', 'Resto UE']
    values  = [poblacion_iberia, poblacion_resto]       # ← no % aquí
    colors  = ['#f30000', '#00145A']
    
    fig1 = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        customdata=customdata,
        hole=0.6,
        marker=dict(colors=colors),
        textinfo='percent',
        textfont=dict(color='white', size=15),
        hovertemplate='<b>%{label}</b><br>Población: %{customdata}<extra></extra>'
    )])

    fig1.update_layout(
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=150),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    config_plotly = {
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "zoom2d", "pan2d", "select2d", "lasso2d",
            "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian", "toImage"
        ]
    }
    
    st.plotly_chart(fig1, use_container_width=True, config=config_plotly, key="chart_poblacion")    

# Fuerza Laboral
with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <p style="font-size: 35px; font-weight: bold; margin-bottom: 1px;">Fuerza Laboral</p>
            <p style="font-size: 20px; font-weight: light;">% Iberia vs UE</p>
            <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;'>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #f30000;'></div>
                    <span>Iberia {0:.1f}%</span>
                </div>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #00145A;'></div>
                    <span>UE {1:.1f}%</span>
                </div>
            </div>
        </div>
    """.format(porc_fuerza_iberia, porc_fuerza_ue), unsafe_allow_html=True)
    

    df_barras_plotly = pd.DataFrame({
        'PAIS': ['Portugal', 'España', 'UE'],
        'VALOR': [fuerza_portugal, fuerza_espana, fuerza_ue]
    })

    # Crear textos abreviados y hover con formato ES
    df_barras_plotly["TEXT"] = df_barras_plotly["VALOR"].apply(lambda x: f"{x/1_000_000:.1f}M".replace('.', ','))
    df_barras_plotly["HOVER"] = df_barras_plotly["VALOR"].apply(lambda x: f"{int(x):,}".replace(",", "."))

    # Ordenar de mayor a menor
    df_barras_plotly = df_barras_plotly.sort_values(by='VALOR', ascending=False)

    # Pasar customdata directamente
    fig2 = px.bar(
        df_barras_plotly,
        x='VALOR',
        y='PAIS',
        orientation='h',
        text='TEXT',
        color='PAIS',
        custom_data=["HOVER"],  # <-- Aquí pasamos los datos correctos
        color_discrete_map={
            'UE': '#00145A',
            'España': '#1D57FB',
            'Portugal': '#C6D9DA'
        }
    )

    fig2.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Población: %{customdata[0]}<extra></extra>',
        cliponaxis=False,
        marker=dict(line=dict(width=0))
    )


    fig2.update_layout(
        dragmode=False,
        bargap=0.2,  # << aumenta separación entre barras
        height=270,  # << reduce altura total del gráfico
        xaxis_showticklabels=False,
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=20)
    )

    config_plotly = {
        "displaylogo": False,
        "modeBarButtonsToRemove": [
            "zoom2d", "pan2d", "select2d", "lasso2d",
            "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
            "hoverClosestCartesian", "hoverCompareCartesian", "toImage"
        ]
    }

    st.plotly_chart(fig2, use_container_width=True, config=config_plotly, key="chart_fuerza")


    # Leyenda Fuerza laboral
    st.markdown("""
    <div style='color: #555; text-align: left; margin: 10px 50px 50px 50px;'>
        <p style='font-size: 12px;'> <b>Fuerza laboral:</b> Conjunto de personas en edad de trabajar que están empleadas o que están buscando activamente empleo.</p>
    </div>
    """, unsafe_allow_html=True)


# Desempleo
with col3:
    st.markdown("""
        <div style='text-align: center;'>
            <p style="font-size: 35px; font-weight: bold; margin-bottom: 1px;">Desempleo</p>
            <p style="font-size: 20px; font-weight: light;">% Iberia vs UE</p>
            <div style='display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;'>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #f30000;'></div>
                    <span>Iberia {0:.1f}%</span>
                </div>
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <div style='width: 12px; height: 12px; background-color: #00145A;'></div>
                    <span>UE {1:.1f}%</span>
                </div>
            </div>
        </div>
    """.format(porc_desemp_iberia, porc_desemp_ue), unsafe_allow_html=True)

    # Crear DataFrame y campos personalizados
    df_barras_plotly3 = pd.DataFrame({
        'PAIS': ['Portugal', 'España', 'UE'],
        'VALOR': [desemp_portugal, desemp_espana, desemp_ue]
    })

    df_barras_plotly3["TEXT"] = df_barras_plotly3["VALOR"].apply(lambda x: f"{x/1_000_000:.1f}M".replace('.', ','))
    df_barras_plotly3["HOVER"] = df_barras_plotly3["VALOR"].apply(lambda x: f"{int(x):,}".replace(",", "."))

    # Ordenar de mayor a menor
    df_barras_plotly3 = df_barras_plotly3.sort_values(by='VALOR', ascending=False)

    # Crear gráfico
    fig3 = px.bar(
        df_barras_plotly3,
        x='VALOR',
        y='PAIS',
        orientation='h',
        text='TEXT',
        color='PAIS',
        custom_data=["HOVER"],
        color_discrete_map={
            'UE': '#00145A',
            'España': '#1D57FB',
            'Portugal': '#C6D9DA'
        }
    )

    # Personalización
    fig3.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Población: %{customdata[0]}<extra></extra>',
        cliponaxis=False,
        marker=dict(line=dict(width=0))
    )


    fig3.update_layout(
        dragmode=False,
        bargap=0.2,
        height=270,
        xaxis_showticklabels=False,
        yaxis_title=None,
        xaxis_title=None,
        showlegend=False,
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=20, b=20)
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
    st.plotly_chart(fig3, use_container_width=True, config=config_plotly, key="chart_desempleo")

    # Leyenda desempleo
    st.markdown("""
    <div style='color: #555; text-align: left; margin: 10px 50px 50px 50px;'>
        <p style='font-size: 12px;'> <b>Desempleo:</b> Conjunto de personas en edad de trabajar que no están empleadas, están disponibles para trabajar y han buscado activamente empleo.</p>
    </div>
    """, unsafe_allow_html=True)



    
# Última actualización: Mon Jun 16 14:32:52 UTC 2025
# Última actualización: Mon Jun 16 14:50:47 UTC 2025
# Última actualización: Mon Jun 16 15:38:57 UTC 2025
# Última actualización: Tue Jun 17 07:40:34 UTC 2025
# Última actualización: Tue Jun 17 07:53:27 UTC 2025
# Última actualización: Tue Jun 17 09:13:15 UTC 2025
# Última actualización: Wed Jun 18 11:23:00 UTC 2025
# Última actualización: Thu Jun 19 05:25:53 UTC 2025
# Última actualización: Thu Jun 19 13:29:22 UTC 2025
# Última actualización: Thu Jun 19 14:31:42 UTC 2025
# Última actualización: Mon Jun 23 14:57:19 UTC 2025
# Última actualización: Tue Jun 24 05:27:23 UTC 2025
# Última actualización: Tue Jun 24 11:32:44 UTC 2025
# Última actualización: Wed Jun 25 05:26:56 UTC 2025
# Última actualización: Thu Jun 26 05:26:58 UTC 2025
# Última actualización: Fri Jun 27 05:26:35 UTC 2025
# Última actualización: Sat Jun 28 05:25:45 UTC 2025
# Última actualización: Sun Jun 29 05:27:41 UTC 2025
# Última actualización: Mon Jun 30 05:28:56 UTC 2025
# Última actualización: Tue Jul  1 05:29:18 UTC 2025
# Última actualización: Wed Jul  2 05:28:51 UTC 2025
# Última actualización: Thu Jul  3 05:29:13 UTC 2025
# Última actualización: Fri Jul  4 05:28:26 UTC 2025
# Última actualización: Sat Jul  5 05:25:18 UTC 2025
# Última actualización: Sun Jul  6 05:25:55 UTC 2025
# Última actualización: Mon Jul  7 05:29:35 UTC 2025
# Última actualización: Tue Jul  8 05:27:19 UTC 2025
# Última actualización: Wed Jul  9 05:30:40 UTC 2025
# Última actualización: Thu Jul 10 05:29:13 UTC 2025
# Última actualización: Fri Jul 11 05:29:13 UTC 2025
# Última actualización: Sat Jul 12 05:26:26 UTC 2025
# Última actualización: Sun Jul 13 05:27:44 UTC 2025
# Última actualización: Mon Jul 14 05:31:35 UTC 2025
# Última actualización: Tue Jul 15 05:30:55 UTC 2025
# Última actualización: Wed Jul 16 05:32:15 UTC 2025
# Última actualización: Thu Jul 17 05:30:49 UTC 2025
# Última actualización: Fri Jul 18 05:32:11 UTC 2025
# Última actualización: Sat Jul 19 05:27:45 UTC 2025
