from myfunctions import *
import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import plotly.figure_factory as ff

# ------------------------
villes = ['Lagos', 'Johannesburg', 'Accra', 'Abidjan', 'London', 'Paris', 'Milan', 'Los Angeles', 'New York', 'Mexico', 'São Paulo', 'Santiago', 'Beijing', 'Delhi', 'Tokyo']
indicateurs = ['co', 'pm10', 'o3', 'so2', 'no2', 'pm25','aqi', 'temperature', 'humidity', 'pressure']
city_name = "Abidjan"

st.set_page_config(page_title="Analyse de la qualite de l'air",
                   page_icon="images/air-quality-sensor.png",
                   layout='wide',
                    initial_sidebar_state='collapsed')

@st.cache_data
def get_data():
    df = pd.read_csv('data/world_aqi_data.csv')
    df['Date']= pd.to_datetime(df['Date'])
    df.drop(columns=['Unnamed: 0'], inplace=True)
    return df

df = get_data()
df_carte = df.copy(deep=True)

# charger le contenu du fichier CSS
with open(os.path.join('static', 'styles.css')) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
with st.sidebar:
    st.write("# Parametres:")
    year_filter = st.selectbox(label = "Année:",
                                options = df['year'].unique(),
                                index= 9)
    # month_filter = st.multiselect(label= "Mois:",
    #                         options = df['month_label'].unique(),
    #                         default =df['month_label'].unique())
    city_filter = st.selectbox(label= "Ville:",
                        options=df['City'].unique(),
                        index= 5)
    polluants_filter = st.selectbox(label = "Polluants:",
                                options = ['pm25', 'pm10', 'o3', 'so2', 'no2', 'co'],
                                index= 0)
    meteo_filter = st.selectbox(label = "Variables météorologiques.:",
                                options = ['temperature', 'humidité', 'pression atmosphérique'],
                                index= 0)

df1 = df.query('year == @year_filter & City in @city_filter')
df_city = df.query("City == @city_filter")
df_city['YearMonth'] = df_city['Date'].dt.to_period('M')
# total = float(df)

header_left,header_mid,header_right = st.columns([1,2,1],gap='large')
with header_mid:
    st.write("# Analyse de la qualite de l'air")

st.write("<hr>", unsafe_allow_html=True)
st.write("<h2>1. Vue de la qualité de l'air en temps réel</h3>", unsafe_allow_html=True)
st.write("<p>Aujourd'hui <i>15 juin 2024 à 10h</i>.</p>", unsafe_allow_html=True)

if 'real_aqi_dict' not in st.session_state:
    st.session_state['real_aqi_dict'] = {city_name:get_real_aqi(city_name) for city_name in ['Abidjan', 'London', 'New York', 'Delhi',]}
    
metric1, metric2, metric3, metric4 = st.columns(4, gap='large')

with metric1:
    aqi_cat, icon = aqi_category(st.session_state.real_aqi_dict.get('Abidjan'))
    # st.markdown('<div class="metric-column">', unsafe_allow_html=True)
    st.write("### Abidjan")
    st.image(f"images/{icon}", width=100)
    st.metric(label="Cote d'Ivoire", value=st.session_state.real_aqi_dict.get('Abidjan'))
    # st.markdown('</div>', unsafe_allow_html=True)

with metric2:
    aqi_cat, icon = aqi_category(st.session_state.real_aqi_dict.get('London'))
    st.write("### London")
    st.image(f"images/{icon}", width=100)
    st.metric(label="Angleterre", value=st.session_state.real_aqi_dict.get('London'))

with metric3:
    aqi_cat, icon = aqi_category(st.session_state.real_aqi_dict.get('New York'))
    st.write("### New York")
    st.image(f"images/{icon}", width=100)
    st.metric(label="Etat Unis d'Amerique", value=st.session_state.real_aqi_dict.get('New York'))
    
with metric4:
    aqi_cat, icon = aqi_category(st.session_state.real_aqi_dict.get('Delhi'))
    st.write("### Delhi")
    st.image(f"images/{icon}", width=100)
    st.metric(label="Inde", value=st.session_state.real_aqi_dict.get('Delhi'))
    
st.write("<hr>", unsafe_allow_html=True)
st.write("# 2. Analyse: ")

st.write("## 2.1 Appercu des donnees: ")
st.write("Dimensions:",df1.shape)
st.dataframe(df1)

st.write("## 2.2 Statistiques descriptives: ")
st.dataframe(df1[['co', 'pm10', 'o3', 'so2', 'no2', 'pm25', 'humidity', 'pressure', 'temperature', 'wind']].describe())

st.write("## 2.3 Description des polluants")
schema = ['Date', 'year', 'month', 'month_label', 'Continent_name', 'Country_name', 'City']
df2 = df1[schema + indicateurs]
df3 = df2.groupby(by=['year', 'month', 'month_label']).mean(numeric_only=True)[polluants_filter].reset_index()   

polluant1, polluant2 = st.columns([1,2], gap='large')
with polluant1:
    pol_mean = round(df3[polluants_filter].mean(),2)
    pol_min = round(df3[polluants_filter].min(),2)
    pol_max = round(df3[polluants_filter].max(),2)
    pol_var = round(df3[polluants_filter].var(),2)
    st.write(f"### Description du polluant: {polluants_filter}")
    st.write(f"- Moyenne: ***{pol_mean}***")
    st.write(f"- Variance: ***{pol_var}***")
    st.write(f"- Min: ***{pol_min}***")
    st.write(f"- Max: ***{pol_max}***")
    st.write(f"#### {get_polluant_description(polluants_filter)}")
    
    

with polluant2:    
    # df3 = df2.groupby(by=['year', 'month_label', 'specie']).max(numeric_only=True)['value'].reset_index()    
    fige_line = px.line(df3, x='month', y=polluants_filter, title='<b>Pollutants Over Months</b>')
    fige_line.update_xaxes(rangeslider_visible=True)
    fige_line.update_layout(title={'x': 0.5}, plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    # fige_line = px.bar(df3,
    #                     x='month',
    #                     y='value',
    #                     title='<b>Click Through Rate</b>')
    # fige_line.update_layout(title = {'x' : 0.5},
    #                                 plot_bgcolor = "rgba(0,0,0,0)",
    #                                 xaxis =(dict(showgrid = False)),
                                    # yaxis =(dict(showgrid = False)))
    st.plotly_chart(fige_line,use_container_width=True)

month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df1['month_label'] = pd.Categorical(df1['month_label'], categories=month_order, ordered=True)
fig_bar = px.bar(df1.groupby('month_label')[polluants_filter].mean().reset_index(), x='month_label', y=polluants_filter,
             title=f'Niveaux Moyens de {polluants_filter}  par Mois')
st.plotly_chart(fig_bar, use_container_width=True)

st.write("## 2.4 Tendance et variation saisonniere des polluants")
trend1, trend2 = st.columns([2,1], gap='large')
with trend1:
    df_city['YearMonth'] = pd.to_datetime(df_city['YearMonth'].astype(str), format='%Y-%m')
    df_city_trend = df_city.groupby(by=['YearMonth']).mean(numeric_only=True)[indicateurs]
    decomposition = seasonal_decompose(df_city_trend[polluants_filter], model='additive', period=12)
    decomposition_df = pd.DataFrame({
        'Observed': decomposition.observed,
        'Trend': decomposition.trend,
        'Seasonal': decomposition.seasonal,
        'Residual': decomposition.resid
    })
    decomposition_df = decomposition_df.reset_index()
    decomposition_df['YearMonth'] = df_city_trend.index
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=decomposition_df['YearMonth'], y=decomposition_df['Observed'], mode='lines', name='Observeé'))
    fig.add_trace(go.Scatter(x=decomposition_df['YearMonth'], y=decomposition_df['Trend'], mode='lines', name='Tendance'))
    fig.add_trace(go.Scatter(x=decomposition_df['YearMonth'], y=decomposition_df['Seasonal'], mode='lines', name='Saisonalité'))
    fig.add_trace(go.Scatter(x=decomposition_df['YearMonth'], y=decomposition_df['Residual'], mode='lines', name='Residu'))
    fig.update_layout(
        title=f'Décomposition des niveaux de {polluants_filter} pour {city_filter}',
        xaxis_title='YearMonth',
        yaxis_title=f'{polluants_filter}',
        legend_title='Composantes de tendance',
        template='plotly_dark'
    )
    st.plotly_chart(fig, use_container_width=True)
with trend2:
    st.write("""
             ### Explication des composantes:
            - **Observée** : Permet de voir la série temporelle dans son ensemble, avec toutes ses variations.
            - **Tendance** : Permet de comprendre la direction générale de l'évolution de la série.
            - **Saisonnière** : Permet de détecter des motifs récurrents dans les données.
            - **Résiduelle** : Permet d'identifier des anomalies ou des variations non expliquées par la tendance et la saisonnalité.
             """)

st.write("## 2.5 Cartographie des polluants")
df_carte['iso_alpha'] = df_carte['Country_name'].map(country_iso_alpha_3)
df_carte['YearMonth'] = df_carte['Date'].dt.to_period('M')
carte1, carte2 = st.columns([2, 2], gap='large')
with carte1:
    carte_fig1 = px.choropleth(
        df_carte,
        locations='iso_alpha',
        color=f'{polluants_filter}',
        hover_name='Country_name',
        animation_frame='YearMonth',
        hover_data={'aqi': True, 'iso_alpha': False},
        projection='natural earth',
        title=f'Répartition géographique des niveaux moyens de {polluants_filter} par pays',
        color_continuous_scale= "Reds")
    st.plotly_chart(carte_fig1, use_container_width=True)
    
with carte2:
    # st.write("### Analyse spaiale de lapollutions de l'air")
    carte_fig2 = px.scatter_geo(df_carte, locations='iso_alpha', color='aqi', hover_name='City',
                     projection='orthographic', title='Répartition Géographique des Niveaux de Pollution')
    st.plotly_chart(carte_fig2, use_container_width=True)


st.write("<hr>", unsafe_allow_html=True)
st.write("# 3. Etude comparative et de correlation: ")

st.write("## 3.1 Etude comparative: periode Pre-COVI vs Post-COVID ")
# df_precovid = df_city_covid.query("year < 2020 & month < 3")
# df_postcovid = df_city_covid.query("year >= 2020 & month >= 3")


df_city['periode'] = ['post-covid' if date >= '2020-03' else 'pre-covid' for date in df_city['YearMonth'].astype(str)]
df_city['YearMonth'] = df_city['YearMonth'].astype(str)
df_monthly_covid = df_city.groupby(by=['YearMonth','periode']).mean(numeric_only=True)['aqi'].reset_index()

# precovid, postcovid = st.columns([2,2], gap='large')

# with precovid:
fige_line_precovid = px.line(df_monthly_covid, x='YearMonth', y='aqi', color='periode', title=f"<b>Pollution de l'air pre-COVID: {city_filter}</b>")
fige_line_precovid.update_xaxes(rangeslider_visible=True)
fige_line_precovid.update_layout(title={'x': 0.5}, plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=True), yaxis=dict(showgrid=False))
st.plotly_chart(fige_line_precovid,use_container_width=True)
    # st.dataframe(df_precovid)
# with postcovid:
#     fige_line_postcovid = px.line(df_postcovid, x='Date', y='aqi', title=f"<b>Pollution de l'air post-COVID: {city_filter}</b>")
#     fige_line_postcovid.update_xaxes(rangeslider_visible=True)
#     fige_line_postcovid.update_layout(title={'x': 0.5}, plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
#     st.plotly_chart(fige_line_postcovid,use_container_width=True)
#     # st.dataframe(df_postcovid)

st.write("## 3.2 Etude comparative inter-ville ")
continent_filter = st.selectbox(label="Continent:", options=df['Continent_name'].unique(), index=1)
df_continent = df.query("Continent_name == @continent_filter")
df_continent['YearMonth'] = df_continent['Date'].dt.to_period('M')
df_continent['YearMonth'] = df_continent['YearMonth'].astype(str)
df_monthly_continent = df_continent.groupby(by=['YearMonth', 'City']).mean(numeric_only=True)['aqi'].reset_index()

desc_ville, graphe_ville = st.columns([1, 2], gap='large')
with desc_ville:
    # st.write("### Description des villes:")
    # for city in df_monthly_continent['City'].unique():
    #     st.write(f"#### {city} / {get_city_description(city)}")
    # df_continent_box = df.query("Continent_name == @continent_filter")
    fig_box = px.box(df_continent, x='City', y=polluants_filter, title='Distribution des Niveaux de Pollution par Ville')
    st.plotly_chart(fig_box,use_container_width=True)

        
with graphe_ville:
    st.write("### Courbes de comparaison:")
    fige_line_continent = px.line(df_monthly_continent, x='YearMonth', y='aqi', color='City', title=" ")
    fige_line_continent.update_xaxes(rangeslider_visible=True)
    fige_line_continent.update_layout(title={'x': 0.5}, plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=True), yaxis=dict(showgrid=False))
    st.plotly_chart(fige_line_continent,use_container_width=True)
# st.dataframe(df_continent)

st.write("<hr>", unsafe_allow_html=True)
st.write("# 4. Analyse de correlation: ")
correlation_matrix = df1[['co', 'pm10', 'o3', 'so2', 'no2', 'pm25']].corr()

# Créer une heatmap pour visualiser la matrice de corrélation
corr_fig = ff.create_annotated_heatmap(
    z=correlation_matrix.values,
    x=correlation_matrix.columns.tolist(),
    y=correlation_matrix.columns.tolist(),
    colorscale='Viridis')
fig.update_layout(
    title='Matrice de Corrélation entre les Polluants',
    xaxis_title='Polluants',
    yaxis_title='Polluants'
)
st.plotly_chart(corr_fig,use_container_width=True)