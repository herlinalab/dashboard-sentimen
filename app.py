import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from collections import Counter
import re

# =====================================
# CONFIG PAGE
# =====================================
st.set_page_config(
    page_title="Analisis Sentimen WFH ASN",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.04);
        border-right: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }

    /* Header hero */
    .hero-container {
        background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.15));
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #a5b4fc;
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(99,102,241,0.3);
        border: 1px solid rgba(99,102,241,0.5);
        color: #a5b4fc;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(20px);
        transition: transform 0.2s, border-color 0.2s;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-color: rgba(99,102,241,0.4);
    }
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent);
        border-radius: 0 0 16px 16px;
    }
    .metric-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .metric-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-pct {
        font-size: 0.8rem;
        margin-top: 0.25rem;
        font-weight: 600;
    }

    /* Section headers */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    /* Chart wrappers */
    .chart-wrapper {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }

    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(168,85,247,0.1));
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        color: #e2e8f0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .insight-title {
        font-weight: 700;
        color: #a5b4fc;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }

    /* Top keywords */
    .keyword-chip {
        display: inline-block;
        background: rgba(99,102,241,0.2);
        border: 1px solid rgba(99,102,241,0.35);
        color: #c7d2fe;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 0.2rem;
    }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* Streamlit component overrides */
    [data-testid="metric-container"] {
        background: transparent !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: opacity 0.2s !important;
    }
    .stDownloadButton > button:hover {
        opacity: 0.85 !important;
    }
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(99,102,241,0.4) !important;
    }
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    df = pd.read_csv("hasil_sentimen.csv")
    df['sentiment_label'] = df['sentiment'].map({
        1: 'Positif',
        0: 'Negatif',
        2: 'Netral'
    })
    return df

df = load_data()

# Color scheme
COLORS = {
    'Positif': '#22c55e',
    'Negatif': '#ef4444',
    'Netral':  '#f59e0b'
}
PLOTLY_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor':  'rgba(0,0,0,0)',
    'font_color':    '#e2e8f0',
    'gridcolor':     'rgba(255,255,255,0.06)',
}

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.markdown("### 🏛️ Dashboard WFH ASN")
    st.markdown("---")
    st.markdown("**⚙️ Filter Data**")
    selected_sentiment = st.multiselect(
        "Pilih Sentimen",
        options=df['sentiment_label'].unique(),
        default=df['sentiment_label'].unique()
    )
    st.markdown("---")
    st.markdown("**📌 Tentang Dashboard**")
    st.markdown(
        "<small style='color:#94a3b8'>Analisis sentimen komentar Instagram terkait kebijakan WFH ASN di hari Jumat.</small>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    total_all = len(df)
    st.markdown(f"<small style='color:#94a3b8'>Total keseluruhan data: <b style='color:#a5b4fc'>{total_all:,}</b></small>", unsafe_allow_html=True)

# =====================================
# FILTER DATA
# =====================================
filtered_df = df[df['sentiment_label'].isin(selected_sentiment)]

# =====================================
# HERO HEADER
# =====================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">📊 Analisis Sentimen · Instagram</div>
    <h1 class="hero-title">Perspektif Masyarakat Terhadap<br>Kebijakan WFH ASN di Hari Jumat</h1>
    <p class="hero-subtitle">Eksplorasi interaktif sentimen publik berdasarkan komentar media sosial · Dibuat dengan Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# METRIC CARDS (HTML custom)
# =====================================
total_data = len(filtered_df)
positif  = (filtered_df['sentiment'] == 1).sum()
negatif  = (filtered_df['sentiment'] == 0).sum()
netral   = (filtered_df['sentiment'] == 2).sum()

pct_pos = round(positif / total_data * 100, 1) if total_data else 0
pct_neg = round(negatif / total_data * 100, 1) if total_data else 0
pct_net = round(netral  / total_data * 100, 1) if total_data else 0

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "📦", total_data, "Total Komentar", "100%",  "#6366f1"),
    (c2, "😊", positif,    "Positif",         f"{pct_pos}%", "#22c55e"),
    (c3, "😠", negatif,    "Negatif",         f"{pct_neg}%", "#ef4444"),
    (c4, "😶", netral,     "Netral",          f"{pct_net}%", "#f59e0b"),
]
for col, icon, val, label, pct, color in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card" style="--accent:{color}">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{val:,}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-pct" style="color:{color}">{pct}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# ROW 1 — BAR + DONUT
# =====================================
st.markdown('<div class="section-header">📈 Distribusi Sentimen</div>', unsafe_allow_html=True)

sentiment_count = (
    filtered_df['sentiment_label']
    .value_counts()
    .reset_index()
)
sentiment_count.columns = ['Sentimen', 'Jumlah']

col_r1a, col_r1b = st.columns(2)

with col_r1a:
    fig_bar = px.bar(
        sentiment_count, x='Sentimen', y='Jumlah',
        color='Sentimen',
        color_discrete_map=COLORS,
        text='Jumlah',
        title='Jumlah Komentar per Sentimen'
    )
    fig_bar.update_traces(textposition='outside', textfont_size=14, marker_line_width=0)
    fig_bar.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        showlegend=False,
        title_font_size=15,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        margin=dict(t=50, b=30)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_r1b:
    fig_pie = px.pie(
        sentiment_count, values='Jumlah', names='Sentimen',
        color='Sentimen',
        color_discrete_map=COLORS,
        title='Proporsi Sentimen (%)',
        hole=0.55
    )
    fig_pie.update_traces(
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>%{value} komentar<br>%{percent}<extra></extra>'
    )
    fig_pie.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=15,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.15),
        margin=dict(t=50, b=30)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# =====================================
# ROW 2 — HORIZONTAL BAR + GAUGE
# =====================================
col_r2a, col_r2b = st.columns(2)

with col_r2a:
    fig_hbar = go.Figure(go.Bar(
        x=[positif, netral, negatif],
        y=['Positif', 'Netral', 'Negatif'],
        orientation='h',
        marker_color=['#22c55e', '#f59e0b', '#ef4444'],
        text=[f'{positif} ({pct_pos}%)', f'{netral} ({pct_net}%)', f'{negatif} ({pct_neg}%)'],
        textposition='outside'
    ))
    fig_hbar.update_layout(
        title='Perbandingan Horizontal',
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=15,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        margin=dict(t=50, b=30)
    )
    st.plotly_chart(fig_hbar, use_container_width=True)

with col_r2b:
    # Sentiment score -100 to +100
    score = round((positif - negatif) / total_data * 100, 1) if total_data else 0
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={'reference': 0, 'valueformat': '.1f'},
        title={'text': "Sentiment Score", 'font': {'size': 15, 'color': '#e2e8f0'}},
        number={'suffix': '', 'font': {'size': 36, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [-100, 100], 'tickcolor': '#94a3b8'},
            'bar': {'color': '#6366f1'},
            'steps': [
                {'range': [-100, -33], 'color': 'rgba(239,68,68,0.25)'},
                {'range': [-33, 33],   'color': 'rgba(245,158,11,0.2)'},
                {'range': [33, 100],   'color': 'rgba(34,197,94,0.25)'},
            ],
            'threshold': {
                'line': {'color': '#ffffff', 'width': 3},
                'thickness': 0.8,
                'value': score
            },
            'bgcolor': 'rgba(0,0,0,0)',
            'bordercolor': 'rgba(255,255,255,0.1)',
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        margin=dict(t=60, b=20, l=30, r=30),
        height=280
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    score_color = "#22c55e" if score > 0 else "#ef4444" if score < 0 else "#f59e0b"
    sentimen_umum = "cenderung POSITIF" if score > 10 else "cenderung NEGATIF" if score < -10 else "NETRAL / BERIMBANG"
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 Insight Sentimen</div>
        Berdasarkan <b>{total_data:,}</b> komentar yang dianalisis, opini publik
        <b style='color:{score_color}'>{sentimen_umum}</b> terhadap kebijakan WFH ASN.
        Sentiment score: <b style='color:{score_color}'>{score:+.1f}</b> (skala -100 s/d +100).
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# ROW 3 — TOP KEYWORDS BARCHART
# =====================================
st.markdown('<div class="section-header">🔤 Analisis Kata Kunci</div>', unsafe_allow_html=True)

def get_top_words(text_series, n=15, stopwords=None):
    if stopwords is None:
        stopwords = {'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'dengan',
                     'untuk', 'pada', 'adalah', 'tidak', 'ya', 'ada', 'juga',
                     'bisa', 'akan', 'sudah', 'atau', 'lebih', 'tapi', 'kalau',
                     'kita', 'aja', 'sih', 'lah', 'dong', 'nya', 'kan', 'tp',
                     'yg', 'ga', 'gak', 'nggak', 'nih', 'emang', 'banget', 'nan',
                     'pun', 'jadi', 'kalo', 'udah', 'sama', 'lagi', 'mau', 'si'}
    words = []
    for text in text_series.dropna():
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', str(text).lower())
        words.extend([w for w in tokens if w not in stopwords])
    return Counter(words).most_common(n)

col_r3a, col_r3b, col_r3c = st.columns(3)
sentimen_list = [('Positif', col_r3a), ('Netral', col_r3b), ('Negatif', col_r3c)]

for label, col in sentimen_list:
    subset = filtered_df[filtered_df['sentiment_label'] == label]['clean_text']
    if len(subset) > 0:
        top_words = get_top_words(subset, n=10)
        if top_words:
            words_df = pd.DataFrame(top_words, columns=['Kata', 'Frekuensi'])
            fig_kw = px.bar(
                words_df, x='Frekuensi', y='Kata',
                orientation='h',
                color='Frekuensi',
                color_continuous_scale=['rgba(99,102,241,0.4)', COLORS[label]],
                title=f'Top Kata — {label}',
                text='Frekuensi'
            )
            fig_kw.update_traces(textposition='outside')
            fig_kw.update_layout(
                paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
                plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
                font_color=PLOTLY_THEME['font_color'],
                title_font_size=14,
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
                yaxis=dict(autorange='reversed', gridcolor=PLOTLY_THEME['gridcolor']),
                margin=dict(t=50, b=10, l=10, r=10),
                height=350
            )
            with col:
                st.plotly_chart(fig_kw, use_container_width=True)
    else:
        with col:
            st.info(f"Tidak ada data {label}")

# =====================================
# ROW 4 — WORD CLOUD per SENTIMEN
# =====================================
st.markdown('<div class="section-header">☁️ Word Cloud per Sentimen</div>', unsafe_allow_html=True)

wc_cols = st.columns(len(selected_sentiment)) if selected_sentiment else []

wc_color_map = {
    'Positif': ['#134e4a', '#22c55e'],
    'Negatif': ['#450a0a', '#ef4444'],
    'Netral':  ['#451a03', '#f59e0b'],
}

for i, label in enumerate(selected_sentiment):
    subset = filtered_df[filtered_df['sentiment_label'] == label]['clean_text']
    text = " ".join(subset.astype(str))
    if text.strip():
        colors_wc = wc_color_map.get(label, ['#1e1b4b', '#6366f1'])
        cmap = mcolors.LinearSegmentedColormap.from_list("wc", colors_wc)
        wc = WordCloud(
            width=600, height=320,
            background_color=None, mode='RGBA',
            colormap=cmap,
            max_words=100,
            prefer_horizontal=0.8
        ).generate(text)
        fig_wc, ax = plt.subplots(figsize=(6, 3.2))
        fig_wc.patch.set_alpha(0)
        ax.set_facecolor('none')
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"☁️ {label}", color='white', fontsize=12, pad=8)
        with wc_cols[i]:
            st.pyplot(fig_wc, use_container_width=True)

# =====================================
# ROW 5 — TEXT LENGTH DISTRIBUTION
# =====================================
st.markdown('<div class="section-header">📏 Distribusi Panjang Komentar</div>', unsafe_allow_html=True)

filtered_df = filtered_df.copy()
filtered_df['text_length'] = filtered_df['clean_text'].astype(str).apply(len)
filtered_df['word_count']  = filtered_df['clean_text'].astype(str).apply(lambda x: len(x.split()))

col_r5a, col_r5b = st.columns(2)

with col_r5a:
    fig_hist = px.histogram(
        filtered_df, x='text_length',
        color='sentiment_label',
        color_discrete_map=COLORS,
        nbins=40,
        barmode='overlay',
        opacity=0.7,
        title='Distribusi Panjang Karakter Komentar',
        labels={'text_length': 'Jumlah Karakter', 'sentiment_label': 'Sentimen'}
    )
    fig_hist.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=14,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        legend=dict(orientation='h', yanchor='top', y=1.12),
        margin=dict(t=60, b=30)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_r5b:
    fig_box = px.box(
        filtered_df, x='sentiment_label', y='word_count',
        color='sentiment_label',
        color_discrete_map=COLORS,
        title='Sebaran Jumlah Kata per Sentimen',
        labels={'word_count': 'Jumlah Kata', 'sentiment_label': 'Sentimen'},
        points='outliers'
    )
    fig_box.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=14,
        showlegend=False,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        margin=dict(t=50, b=30)
    )
    st.plotly_chart(fig_box, use_container_width=True)

# =====================================
# ROW 6 — TREEMAP + VIOLIN
# =====================================
st.markdown('<div class="section-header">🗂️ Eksplorasi Lanjutan</div>', unsafe_allow_html=True)

col_r6a, col_r6b = st.columns(2)

with col_r6a:
    # Treemap of sentiment
    tree_data = sentiment_count.copy()
    tree_data['parent'] = 'Semua Komentar'
    fig_tree = px.treemap(
        tree_data,
        path=['parent', 'Sentimen'],
        values='Jumlah',
        color='Sentimen',
        color_discrete_map=COLORS,
        title='Treemap Distribusi Sentimen'
    )
    fig_tree.update_traces(
        textinfo='label+value+percent parent',
        hovertemplate='<b>%{label}</b><br>%{value} komentar<br>%{percentParent:.1%}<extra></extra>'
    )
    fig_tree.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=14,
        margin=dict(t=50, b=10)
    )
    st.plotly_chart(fig_tree, use_container_width=True)

with col_r6b:
    fig_vio = px.violin(
        filtered_df, y='text_length', x='sentiment_label',
        color='sentiment_label',
        color_discrete_map=COLORS,
        box=True,
        points='outliers',
        title='Distribusi Panjang Karakter (Violin)',
        labels={'text_length': 'Panjang Karakter', 'sentiment_label': 'Sentimen'}
    )
    fig_vio.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=14,
        showlegend=False,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        margin=dict(t=50, b=30)
    )
    st.plotly_chart(fig_vio, use_container_width=True)

# =====================================
# RINGKASAN STATISTIK
# =====================================
st.markdown('<div class="section-header">📊 Ringkasan Statistik</div>', unsafe_allow_html=True)

stats_cols = st.columns(3)
for i, (label, color) in enumerate(COLORS.items()):
    subset = filtered_df[filtered_df['sentiment_label'] == label]
    with stats_cols[i]:
        avg_len   = round(subset['text_length'].mean(), 1) if len(subset) else 0
        avg_words = round(subset['word_count'].mean(), 1)  if len(subset) else 0
        max_len   = int(subset['text_length'].max()) if len(subset) else 0
        st.markdown(f"""
        <div class="metric-card" style="--accent:{color}; text-align:left; padding:1.2rem 1.5rem">
            <div style="font-weight:700; color:{color}; font-size:1rem; margin-bottom:0.8rem">
                {label}
            </div>
            <div style="color:#94a3b8; font-size:0.8rem; line-height:2">
                📝 Rata-rata karakter: <b style='color:#e2e8f0'>{avg_len}</b><br>
                📖 Rata-rata kata: <b style='color:#e2e8f0'>{avg_words}</b><br>
                📏 Komentar terpanjang: <b style='color:#e2e8f0'>{max_len} karakter</b><br>
                🔢 Total komentar: <b style='color:#e2e8f0'>{len(subset):,}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# DATASET & DOWNLOAD
# =====================================
st.markdown('<div class="section-header">🗂️ Dataset Hasil Analisis</div>', unsafe_allow_html=True)

display_cols = [c for c in ['clean_text', 'sentiment', 'sentiment_label'] if c in filtered_df.columns]
st.dataframe(
    filtered_df[display_cols].reset_index(drop=True),
    use_container_width=True,
    height=300
)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Dataset (CSV)",
    data=csv,
    file_name='hasil_sentimen_filtered.csv',
    mime='text/csv'
)

# =====================================
# FOOTER
# =====================================
st.markdown("<br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    "<div style='text-align:center; color:#475569; font-size:0.8rem; padding:0.5rem'>"
    "Dashboard Analisis Sentimen WFH ASN · Dibuat dengan ❤️ menggunakan Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)
