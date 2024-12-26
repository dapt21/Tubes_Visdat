import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv('dataCovid.csv')

st.title("Kasus Covid di Seluruh Dunia")
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