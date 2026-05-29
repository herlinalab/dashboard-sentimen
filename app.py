import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =====================================
# CONFIG PAGE
# =====================================
st.set_page_config(
    page_title="Dashboard Analisis Sentimen",
    page_icon="📊",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================
df = pd.read_csv("hasil_sentimen.csv")
df['sentiment_label'] = df['sentiment'].map({
    1: 'Positif',
    0: 'Negatif',
    2: 'Netral'
})

# =====================================
# HEADER
# =====================================
st.title("📊 Perspektif Masyarakat Terhadap Kebijakan WFH ASN di Hari Jumat")
st.markdown(
    "analisis sentimen berdasarkan komentar di Instagram."
)

st.divider()

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("⚙️ Menu Dashboard")

selected_sentiment = st.sidebar.multiselect(
    "Filter Sentimen",
    options=df['sentiment_label'].unique(),
    default=df['sentiment_label'].unique()
)

# FILTER DATA
filtered_df = df[df['sentiment_label'].isin(selected_sentiment)]

# =====================================
# METRIC CARDS
# =====================================

total_data = len(filtered_df)

positif = (filtered_df['sentiment'] == 1).sum()
netral = (filtered_df['sentiment'] == 2).sum()
negatif = (filtered_df['sentiment'] == 0).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Data", total_data)
col2.metric("😊 Positif", positif)
col3.metric("😠 Negatif", negatif)
col4.metric("😶 Netral", netral)

# =====================================
# VISUALISASI
# =====================================
st.subheader("📈 Visualisasi Sentimen")

sentiment_count = filtered_df[
    'sentiment_label'
].value_counts().reset_index()

sentiment_count.columns = [
    'Sentimen',
    'Jumlah'
]
col_chart1, col_chart2 = st.columns(2)

# =====================================
# BAR CHART
# =====================================
with col_chart1:

    fig_bar = px.bar(
    sentiment_count,
    x='Sentimen',
    y='Jumlah',
    color='Sentimen',
    text='Jumlah',
    title='Distribusi Sentimen'
)

fig_bar.update_traces(
    textposition='outside'
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# =====================================
# PIE CHART
# =====================================
with col_chart2:

    fig_pie = px.pie(
    sentiment_count,
    values='Jumlah',
    names='Sentimen',
    title='Persentase Sentimen',
    hole=0.4
)

st.plotly_chart(
    fig_pie,
    use_container_width=True
)

st.divider()

# =====================================
# WORD CLOUD
# =====================================
st.subheader("☁️ Word Cloud")

text = " ".join(filtered_df['clean_text'].astype(str))

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color='white'
).generate(text)

fig_wc, ax = plt.subplots(figsize=(12, 6))

ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")

st.pyplot(fig_wc)

st.divider()

# =====================================
# DATASET
# =====================================
st.subheader("🗂️ Dataset Hasil Analisis")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================
# DOWNLOAD CSV
# =====================================
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Download Dataset",
    data=csv,
    file_name='hasil_sentimen_filtered.csv',
    mime='text/csv'
)

# =====================================
# FOOTER
# =====================================
st.divider()

st.caption("Dashboard dibuat menggunakan Streamlit 🚀")
