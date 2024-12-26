import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv('dataCovid.csv')

st.title("Kasus Covid di Seluruh Dunia")
st.write("""
Virus Corona atau Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2) 
adalah virus yang menyerang sistem pernapasan. Virus ini menyebabkan gangguan 
ringan pada sistem pernapasan, infeksi paru-paru yang berat, hingga kematian 
dan virus ini dapat menyerang siapa saja, mulai dari lansia, orang dewasa, anak-anak, bayi.
""", )

fig = px.choropleth(
    data, 
    locationmode="country names", 
    locations="Country/Region", 
    color="TotalDeaths",
    hover_name="Country/Region",
    hover_data="TotalDeaths",
    color_continuous_scale=px.colors.sequential.Plasma,
)
st.plotly_chart(fig)