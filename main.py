import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_lottie import st_lottie
import json
import plotly.graph_objects as go

def get_lottieImg(path):
    with open(path, 'r') as f:
        return json.load(f)

data = pd.read_csv('dataCovid.csv')

st.title("Kasus Covid di Seluruh Dunia")
col1, col2 = st.columns([18, 4])
with col1:
    st.write("""
    Virus Corona atau Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2) 
    adalah virus yang menyerang sistem pernapasan. Virus ini menyebabkan gangguan 
    ringan pada sistem pernapasan, infeksi paru-paru yang berat, hingga kematian 
    dan virus ini dapat menyerang siapa saja, mulai dari lansia, orang dewasa, anak-anak, bayi.
    """, )
with col2:
    coronaImg = get_lottieImg('assets/Corona.json')
    st_lottie(coronaImg)

col1, col2 = st.columns([20, 8])
with col1:
    fig = px.choropleth(
    data, 
    locationmode="country names", 
    locations="Country/Region", 
    color="TotalDeaths",
    hover_name="Country/Region",
    hover_data="TotalDeaths",
    color_continuous_scale=px.colors.sequential.Plasma,
    )
    fig.update_geos(showcountries=True, countrycolor="darkgrey")
    fig.update_layout(
        title='Total Kematian oleh Covid Diseluruh Dunia', 
        geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'),
        coloraxis_colorbar=dict(
            title='Total Deaths', 
            x=0, y=-0.1, 
            xanchor='left', yanchor='bottom',
            len=0.8
        )
    )
    fig.update_coloraxes(colorbar={'orientation':'h', 'thickness':20, 'y': -0.3, 'x':0.4, 'xanchor': 'center'})
    st.plotly_chart(fig)
with col2:
    temp = data.sort_values(by='TotalDeaths', ascending=False).reset_index(drop=True)[['Country/Region','TotalDeaths']]
    dataPie = temp.iloc[:15]
    dataPie.loc[len(dataPie) + 1] = ['other', int(temp.iloc[15:]['TotalDeaths'].sum(axis=0))]
    dataPie.reset_index(drop=True)

    fig = px.pie(
        dataPie,
        labels="Country/Region",
        values='TotalDeaths',
        names='Country/Region',
    )
    fig.update({"layout_showlegend": False})
    st.plotly_chart(fig)

totalDeath = int(data['TotalDeaths'].sum(axis=0))
st.write("Total kematian yang diakibatkan oleh Covid-19 di seluruh dunia adalah: ", totalDeath, "")