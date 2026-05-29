import streamlit as st
import pandas as pd
import plotly.express as px

# Judul
st.title("Dashboard Analisis Sentimen")

# Load data
df = pd.read_csv("hasil_sentimen.csv")

# Tampilkan data
st.subheader("Dataset")
st.dataframe(df)

# Hitung sentimen
sentiment_count = df['sentiment'].value_counts()

# Visualisasi
fig = px.bar(
    x=sentiment_count.index,
    y=sentiment_count.values,
    color=sentiment_count.index,
    labels={
        'x': 'Sentimen',
        'y': 'Jumlah'
    },
    title='Distribusi Sentimen'
)

st.plotly_chart(fig)
