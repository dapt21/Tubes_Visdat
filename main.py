import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_lottie import st_lottie
import json
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots

def get_lottieImg(path):
    with open(path, 'r') as f:
        return json.load(f)

data = pd.read_csv('covidIndonesia.csv')
data = data[
    [
        'Date', 'Location ISO Code', 
        'Location', 'Longitude', 'Latitude', 
        'Province', 'Island', 'New Cases', 
        'New Deaths', 'New Recovered'
    ]
]
data = data[data['Location'] != 'Indonesia'].reset_index(drop=True)
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')

st.title("Kasus Covid di Indonesia")
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

# indonesia geojson
geojson = requests.get(
    "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province-simple.json"
).json()

# Filter untuk data Plot
dataPlot = pd.DataFrame(columns=['Location ISO Code', 'Location', 'Province', 'Total Cases', 'Total Deaths', 'Total Recovered'])
for isoCode in data['Location ISO Code'].unique():
    temp = {"Location ISO Code": [isoCode], 'Location': [''], 'Province': [''], "Total Cases": [0], "Total Deaths": [0], "Total Recovered": [0]}
    for i in range(len(data)):
        if data['Location ISO Code'][i] == isoCode:
            temp['Location'][0] = data['Location'][i]
            temp['Province'][0] = data['Province'][i].upper()
            temp['Total Cases'][0] += data['New Cases'][i]
            temp['Total Deaths'][0] += data['New Deaths'][i]
            temp['Total Recovered'][0] += data['New Recovered'][i]
    dataPlot = pd.concat([dataPlot, pd.DataFrame(temp)]).reset_index(drop=True)

fig = go.Figure(
    data = go.Choropleth(
        geojson = geojson,
        featureidkey="properties.Propinsi",
        locations = dataPlot['Province'],
        z = dataPlot['Total Deaths'],
        colorscale = "Reds",
        colorbar_title = "Total Kematian",
    )
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title='Total Kematian oleh Covid di Indonesia', 
)
fig.update_coloraxes(colorbar={'orientation':'h', 'thickness':20, 'y': -0.3, 'x':0.4, 'xanchor': 'center'})
st.plotly_chart(fig)

col1, col2 = st.columns([1, 4])
with col1:
    deathImg = get_lottieImg('assets/Death.json')
    st_lottie(deathImg)
with col2:
    totalKematian = dataPlot['Total Deaths'].sum()
    jawaTengah = dataPlot['Total Deaths'][dataPlot['Location']=='Jawa Tengah']
    jawaTimur = dataPlot['Total Deaths'][dataPlot['Location']=='Jawa Timur']
    jawaBarat = dataPlot['Total Deaths'][dataPlot['Location']=='Jawa Barat']
    st.write(f"""
        Total kematian oleh covid-19 di Indonesia mencapai {totalKematian:,}. Pada graph di atas, terdapat 3 kota 
        yang memiliki tingkat kematian terbanyak oleh covid-19: 1. Jawa tengah, 2. Jawa Timur, 3. Jawa barat.
        Total kematian yang diakibatkan oleh covid-19 di Jawa Tengah sebanyak {jawaTengah.iloc[0]:,}, di Jawa Timur sebanyak {jawaTimur.iloc[0]:,}, 
        dan di Jawa Barat sebanyak {jawaBarat.iloc[0]:,}.
    """)

dataBulan = data[
    [
        'Date', 'Province', 'New Cases', 
        'New Deaths', 'New Recovered'
    ]
]

st.subheader('Data Covid Tiap Provinsi')
dataBulan['Date'] = dataBulan['Date'].dt.strftime('%m/%Y')
dataBulan['Date'] = pd.to_datetime(dataBulan['Date'], format='%m/%Y')
dataBulan = dataBulan.groupby(['Date', 'Province']).sum().reset_index()

dataBulan2020 = dataBulan[pd.DatetimeIndex(dataBulan['Date']).year == 2020]
dataBulan2020['Date'] = dataBulan2020['Date'].dt.month_name()

dataBulan2021 = dataBulan[pd.DatetimeIndex(dataBulan['Date']).year == 2021]
dataBulan2021['Date'] = dataBulan2021['Date'].dt.month_name()

dataBulan2022 = dataBulan[pd.DatetimeIndex(dataBulan['Date']).year == 2022]
dataBulan2022['Date'] = dataBulan2022['Date'].dt.month_name()

provinsi = st.selectbox("Pilih provinsi", dataBulan['Province'].unique().tolist(), key = 0)

fig = go.Figure()
fig.add_trace(
    go.Bar(
        x = dataBulan2021['Date'][dataBulan2021['Province'] == provinsi],
        y = dataBulan2021['New Deaths'][dataBulan2021['Province'] == provinsi],
        text = dataBulan2021['New Deaths'][dataBulan2021['Province'] == provinsi],
        name = "Tahun 2021",
        marker_color ='red',
        opacity = 0.6,
        width=0.3,
    )
)
fig.add_trace(
    go.Bar(
        x = dataBulan2020['Date'][dataBulan2020['Province'] == provinsi],
        y = dataBulan2020['New Deaths'][dataBulan2020['Province'] == provinsi],
        text = dataBulan2020['New Deaths'][dataBulan2020['Province'] == provinsi],
        name = "Tahun 2020",
        marker_color = 'orange',
        opacity = 0.6,
        width=0.3,
    )
)
fig.add_trace(
    go.Bar(
        x = dataBulan2022['Date'][dataBulan2022['Province'] == provinsi],
        y = dataBulan2022['New Deaths'][dataBulan2022['Province'] == provinsi],
        text = dataBulan2022['New Deaths'][dataBulan2022['Province'] == provinsi],
        name = "Tahun 2022",
        marker_color = 'blue',
        opacity = 0.6,
        width=0.3,
    )
)
fig.update_traces(
    texttemplate='%{text:.2s}',
    textfont_size=12, 
    textangle=0, 
    textposition="outside", 
    cliponaxis=False,
)
fig.update_layout(
    title=dict(
        text=f'Total Kematian di Provinsi {provinsi} dari bulan ke bulan'
    ),
    xaxis=dict(
        title=dict(
            text='Bulan'
        )
    ),
    yaxis=dict(
        title=dict(
            text='Total Kematian'
        )
    ),
    legend=dict(
        x=0,
        y=1.0,
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
st.plotly_chart(fig)

dataTahun = data[
    [
        'Date', 'Province', 'New Cases', 
        'New Deaths', 'New Recovered'
    ]
]
dataTahun['Date'] = dataTahun['Date'].dt.strftime('%Y')
dataTahun['Date'] = pd.to_datetime(dataTahun['Date'], format='%Y')
dataTahun['Date'] = dataTahun['Date'].dt.year.astype(int)
dataTahun = dataTahun.groupby(['Date', 'Province']).sum().reset_index()

dataTahun2020 = dataTahun[dataTahun['Date'] == 2020]
dataTahun2021 = dataTahun[dataTahun['Date'] == 2021]
dataTahun2022 = dataTahun[dataTahun['Date'] == 2022]

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x = dataTahun2020['Date'][dataTahun2020['Province'] == provinsi],
        y = dataTahun2020['New Deaths'][dataTahun2020['Province'] == provinsi],
        text = dataTahun2020['New Deaths'][dataTahun2020['Province'] == provinsi],
        name = "Tahun 2020",
        marker_color ='orange',
        opacity = 0.6,
        width=0.3,
    )
)
fig.add_trace(
    go.Bar(
        x = dataTahun2021['Date'][dataTahun2021['Province'] == provinsi],
        y = dataTahun2021['New Deaths'][dataTahun2021['Province'] == provinsi],
        text = dataTahun2021['New Deaths'][dataTahun2021['Province'] == provinsi],
        name = "Tahun 2021",
        marker_color ='red',
        opacity = 0.6,
        width=0.3,
    )
)
fig.add_trace(
    go.Bar(
        x = dataTahun2022['Date'][dataTahun2022['Province'] == provinsi],
        y = dataTahun2022['New Deaths'][dataTahun2022['Province'] == provinsi],
        text = dataTahun2022['New Deaths'][dataTahun2022['Province'] == provinsi],
        name = "Tahun 2022",
        marker_color ='blue',
        opacity = 0.6,
        width=0.3,
    )
)

fig.update_traces(
    texttemplate='%{text:.2s}',
    textfont_size=12, 
    textangle=0, 
    textposition="outside", 
    cliponaxis=False,
)
fig.update_layout(
    title=dict(
        text=f'Total Kematian di Provinsi {provinsi} dari tahun ke tahun'
    ),
    xaxis=dict(
        title=dict(
            text='Tahun'
        ),
        tickmode = 'array',
        tickvals = [2020, 2021, 2022],
        ticktext = ["2020", "2021", "2022"],
    ),
    yaxis=dict(
        title=dict(
            text='Total Kematian'
        )
    ),
    legend=dict(
        x=0,
        y=1.0,
    ),
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)
st.plotly_chart(fig)

st.subheader("Apakah covid dapat disembuhkan?")
col1, col2 = st.columns([3, 2])

protectImg = get_lottieImg('assets/Protection.json')
st_lottie(protectImg)

st.write("""
    Iya. pada tahun 2021, menurut WHO terdapat sebanyak 80% total kasus covid yang muncul 
    menimbulkan gejala ringan saja. Artinya, kasus-kasus yang muncul melibatkan gejala 
    ringan, seperti demam, batuk, atau sesak napas yang dapat sembuh dengan sendirinya. 
    Selain tidak menimbulkan gejala yang berarti, maka akan semakin besar pula peluang 
    untuk bisa sembuh dengan lebih cepat. Bagi pengidap positif dengan gejala ringan yang 
    muncul, mereka akan membutuhkan waktu pemulihan selama dua minggu lamanya. 
    Sedangkan gejala dengan intensitas sedang hingga kritis, akan membutuhkan 
    waktu lebih lama lagi, yaitu antara 3-6 minggu masa penyembuhan. Namun pada zaman sekarang,
    vaksin covid-19 telah ditemukan. Tujuan dari vaksin sendiri ialah meningkatkan kekebalan 
    seseorang secara aktif terhadap suatu penyakit, sehingga apabila suatu saat terpajan 
    dengan penyakit tersebut tidak akan sakit atau hanya mengalami sakit ringan dan tidak 
    menjadi sumber penularan.
""")

st.subheader("Lalu, bagaimana perbandingan sembuh dan mati akibat Covid?")
st.write("Berikut adalah graph perbandingan sembuh dan mati yang diakibatkan oleh covid:")

provinsi2 = st.selectbox("Pilih provinsi", dataBulan['Province'].unique().tolist(), key = 1)

angkaMati = dataTahun['New Deaths'][dataTahun['Province'] == provinsi2]
angkaSembuh = dataTahun['New Recovered'][dataTahun['Province'] == provinsi2]
angkaKasus = dataTahun['New Cases'][dataTahun['Province'] == provinsi2]

persenMati = (angkaMati.iloc[0]/angkaKasus.iloc[0]) * 100
persenSembuh = (angkaSembuh.iloc[0]/angkaKasus.iloc[0]) * 100

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x = dataTahun['Date'][dataTahun['Province'] == provinsi2],
        y = dataTahun['New Deaths'][dataTahun['Province'] == provinsi2],
        mode = 'lines+markers',
        name = 'Mati',
        line = dict(
            color = 'red',
            width = 2,
        ),
        opacity = 0.6
    )
)
fig.add_trace(
    go.Scatter(
        x = dataTahun['Date'][dataTahun['Province'] == provinsi2],
        y = dataTahun['New Recovered'][dataTahun['Province'] == provinsi2],
        mode = 'lines+markers',
        name = 'Sembuh',
        line = dict(
            color = 'blue',
            width = 2,
        ),
        opacity = 0.6
    )
)
fig.add_trace(
    go.Scatter(
        x = dataTahun['Date'][dataTahun['Province'] == provinsi2],
        y = dataTahun['New Cases'][dataTahun['Province'] == provinsi2],
        mode = 'lines+markers',
        name = 'Kasus Covid',
        line = dict(
            color = 'orange',
            width = 2,
        ),
        opacity = 0.6
    )
)
fig.update_layout(
    title=dict(
        text=f'Provinsi {provinsi2}, memiliki tingkat mati: {persenMati:.2f}% dan tingkat kesembuhan: {persenSembuh:.2f}%'
    ),
    xaxis = dict(
        tickmode='array', 
        tickvals = dataTahun['Date'][dataTahun['Province'] == provinsi2], 
        ticktext = [2020, 2021, 2022], 
    ),
    font=dict(size=18, color="black")
)
st.plotly_chart(fig)

tyImg = get_lottieImg('assets/ThanksYou.json')
st_lottie(tyImg)