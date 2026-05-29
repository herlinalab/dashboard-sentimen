import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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
# CUSTOM CSS — LIGHT & BRIGHT THEME
# =====================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    /* Background utama — putih bersih + pola titik-titik */
    .stApp {
        background-color: #f0f4ff;
        background-image: radial-gradient(#c7d2fe 1px, transparent 1px);
        background-size: 28px 28px;
        min-height: 100vh;
    }

    /* Sidebar cerah */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6366f1 0%, #818cf8 100%) !important;
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
        background: rgba(255,255,255,0.2) !important;
        border-color: rgba(255,255,255,0.4) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.3) !important;
    }

    /* Hero header */
    .hero-container {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        border-radius: 24px;
        padding: 2.5rem 3rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(99,102,241,0.35);
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 280px; height: 280px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
    }
    .hero-container::after {
        content: '';
        position: absolute;
        bottom: -80px; left: 30%;
        width: 220px; height: 220px;
        background: rgba(255,255,255,0.07);
        border-radius: 50%;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.25);
        border: 1px solid rgba(255,255,255,0.4);
        color: #ffffff;
        padding: 0.25rem 0.9rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.5rem 0;
        line-height: 1.25;
        text-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem;
        font-weight: 500;
        margin: 0;
    }

    /* Metric cards */
    .metric-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 1.5rem 1.2rem;
        text-align: center;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07);
        border-top: 5px solid var(--accent);
        transition: transform 0.2s, box-shadow 0.2s;
        position: relative;
        overflow: hidden;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 32px rgba(0,0,0,0.12);
    }
    .metric-card-bg {
        position: absolute;
        top: -20px; right: -20px;
        width: 80px; height: 80px;
        border-radius: 50%;
        background: var(--accent);
        opacity: 0.08;
    }
    .metric-icon { font-size: 2.2rem; margin-bottom: 0.4rem; }
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1;
        margin-bottom: 0.25rem;
    }
    .metric-label {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .metric-pct {
        font-size: 0.85rem;
        font-weight: 700;
        margin-top: 0.3rem;
        padding: 0.15rem 0.6rem;
        background: color-mix(in srgb, var(--accent) 12%, white);
        border-radius: 10px;
        display: inline-block;
    }

    /* Section headers */
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 800;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 2rem 0 1rem 0;
        padding: 0.7rem 1.2rem;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 4px solid #6366f1;
    }

    /* Chart card wrapper */
    .chart-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 0.5rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    }

    /* Insight box */
    .insight-box {
        background: linear-gradient(135deg, #eff6ff, #faf5ff);
        border: 2px solid #e0e7ff;
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        color: #334155;
        font-size: 0.9rem;
        line-height: 1.7;
        box-shadow: 0 2px 12px rgba(99,102,241,0.1);
    }
    .insight-title {
        font-weight: 800;
        color: #6366f1;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem;
    }

    /* Stats card */
    .stats-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        border-bottom: 4px solid var(--accent);
    }
    .stats-title {
        font-weight: 800;
        font-size: 1rem;
        margin-bottom: 0.8rem;
    }
    .stats-row {
        font-size: 0.82rem;
        color: #64748b;
        line-height: 2;
    }
    .stats-val { color: #1e293b; font-weight: 700; }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.65rem 2.2rem !important;
        font-family: 'Nunito', sans-serif !important;
        font-size: 0.95rem !important;
        box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
        transition: all 0.2s !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(99,102,241,0.5) !important;
    }

    /* Divider */
    hr { border-color: #e2e8f0 !important; }

    /* Dataframe */
    div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.82rem;
        padding: 1rem;
        font-weight: 600;
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

# Warna cerah & vivid
COLORS = {
    'Positif': '#10b981',   # emerald
    'Negatif': '#f43f5e',   # rose
    'Netral':  '#f59e0b',   # amber
}
PLOTLY_THEME = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor':  '#fafafa',
    'font_color':    '#334155',
    'gridcolor':     '#e2e8f0',
}

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:
    st.markdown("### 🏛️ WFH ASN Dashboard")
    st.markdown("---")
    st.markdown("**⚙️ Filter Data**")
    selected_sentiment = st.multiselect(
        "Pilih Sentimen",
        options=df['sentiment_label'].unique(),
        default=df['sentiment_label'].unique()
    )
    st.markdown("---")
    st.markdown("**📌 Tentang**")
    st.markdown(
        "<small>Analisis sentimen komentar Instagram terkait kebijakan WFH ASN di hari Jumat.</small>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown(f"<small>Total data: <b>{len(df):,}</b> komentar</small>", unsafe_allow_html=True)

# =====================================
# FILTER
# =====================================
filtered_df = df[df['sentiment_label'].isin(selected_sentiment)]

# =====================================
# HERO
# =====================================
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">📊 Analisis Sentimen · Instagram</div>
    <h1 class="hero-title">Perspektif Masyarakat Terhadap<br>Kebijakan WFH ASN di Hari Jumat</h1>
    <p class="hero-subtitle">Eksplorasi interaktif sentimen publik berdasarkan komentar media sosial · Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# METRIC CARDS
# =====================================
total_data = len(filtered_df)
positif  = (filtered_df['sentiment'] == 1).sum()
negatif  = (filtered_df['sentiment'] == 0).sum()
netral   = (filtered_df['sentiment'] == 2).sum()
pct_pos  = round(positif / total_data * 100, 1) if total_data else 0
pct_neg  = round(negatif / total_data * 100, 1) if total_data else 0
pct_net  = round(netral  / total_data * 100, 1) if total_data else 0

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "📦", total_data, "Total Komentar", "100%",    "#6366f1"),
    (c2, "😊", positif,    "Positif",         f"{pct_pos}%", "#10b981"),
    (c3, "😠", negatif,    "Negatif",         f"{pct_neg}%", "#f43f5e"),
    (c4, "😶", netral,     "Netral",          f"{pct_net}%", "#f59e0b"),
]
for col, icon, val, label, pct, color in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card" style="--accent:{color}">
            <div class="metric-card-bg"></div>
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
    fig_bar.update_traces(
        textposition='outside', textfont_size=14,
        marker_line_width=0,
        marker_line_color='white'
    )
    fig_bar.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        showlegend=False, title_font_size=15,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor'], showgrid=False),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        margin=dict(t=50, b=30),
        bargap=0.3
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
        pull=[0.05, 0.05, 0.05],
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
# ROW 2 — HBAR + GAUGE
# =====================================
col_r2a, col_r2b = st.columns(2)

with col_r2a:
    fig_hbar = go.Figure(go.Bar(
        x=[positif, netral, negatif],
        y=['Positif', 'Netral', 'Negatif'],
        orientation='h',
        marker_color=['#10b981', '#f59e0b', '#f43f5e'],
        text=[f'{positif} ({pct_pos}%)', f'{netral} ({pct_net}%)', f'{negatif} ({pct_neg}%)'],
        textposition='outside',
        marker_line_width=0
    ))
    fig_hbar.update_layout(
        title='Perbandingan Sentimen (Horizontal)',
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=15,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        yaxis=dict(gridcolor='rgba(0,0,0,0)'),
        margin=dict(t=50, b=30),
        bargap=0.35
    )
    st.plotly_chart(fig_hbar, use_container_width=True)

with col_r2b:
    score = round((positif - negatif) / total_data * 100, 1) if total_data else 0
    score_color = "#10b981" if score > 0 else "#f43f5e" if score < 0 else "#f59e0b"
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={'reference': 0, 'valueformat': '.1f'},
        title={'text': "Sentiment Score", 'font': {'size': 15, 'color': '#334155'}},
        number={'suffix': '', 'font': {'size': 36, 'color': '#1e293b'}},
        gauge={
            'axis': {'range': [-100, 100], 'tickcolor': '#94a3b8'},
            'bar': {'color': score_color},
            'steps': [
                {'range': [-100, -33], 'color': '#fee2e2'},
                {'range': [-33, 33],   'color': '#fef9c3'},
                {'range': [33, 100],   'color': '#dcfce7'},
            ],
            'threshold': {
                'line': {'color': '#334155', 'width': 3},
                'thickness': 0.8, 'value': score
            },
            'bgcolor': 'white',
            'bordercolor': '#e2e8f0',
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        margin=dict(t=60, b=20, l=30, r=30),
        height=280
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

    sentimen_umum = "cenderung <b style='color:#10b981'>POSITIF</b>" if score > 10 \
        else "cenderung <b style='color:#f43f5e'>NEGATIF</b>" if score < -10 \
        else "<b style='color:#f59e0b'>NETRAL / BERIMBANG</b>"
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">💡 Insight Sentimen</div>
        Dari <b>{total_data:,}</b> komentar yang dianalisis, opini publik
        {sentimen_umum} terhadap kebijakan WFH ASN.
        Sentiment score: <b style='color:{score_color}'>{score:+.1f}</b> (skala −100 s/d +100).
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# ROW 3 — TOP KEYWORDS
# =====================================
st.markdown('<div class="section-header">🔤 Analisis Kata Kunci per Sentimen</div>', unsafe_allow_html=True)

def get_top_words(text_series, n=10):
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
kw_color_scales = {
    'Positif': ['#d1fae5', '#10b981'],
    'Negatif': ['#ffe4e6', '#f43f5e'],
    'Netral':  ['#fef3c7', '#f59e0b'],
}
for label, col in [('Positif', col_r3a), ('Netral', col_r3b), ('Negatif', col_r3c)]:
    subset = filtered_df[filtered_df['sentiment_label'] == label]['clean_text']
    if len(subset) > 0:
        top_words = get_top_words(subset, n=10)
        if top_words:
            words_df = pd.DataFrame(top_words, columns=['Kata', 'Frekuensi'])
            fig_kw = px.bar(
                words_df, x='Frekuensi', y='Kata',
                orientation='h',
                color='Frekuensi',
                color_continuous_scale=kw_color_scales[label],
                title=f'Top 10 Kata — {label}',
                text='Frekuensi'
            )
            fig_kw.update_traces(textposition='outside', marker_line_width=0)
            fig_kw.update_layout(
                paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
                plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
                font_color=PLOTLY_THEME['font_color'],
                title_font_size=14,
                showlegend=False,
                coloraxis_showscale=False,
                xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
                yaxis=dict(autorange='reversed', gridcolor='rgba(0,0,0,0)'),
                margin=dict(t=50, b=10, l=10, r=30),
                height=340
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
    'Positif': ['#a7f3d0', '#059669'],
    'Negatif': ['#fecdd3', '#e11d48'],
    'Netral':  ['#fde68a', '#d97706'],
}

for i, label in enumerate(selected_sentiment):
    subset = filtered_df[filtered_df['sentiment_label'] == label]['clean_text']
    text = " ".join(subset.astype(str))
    if text.strip():
        cmap = mcolors.LinearSegmentedColormap.from_list("wc", wc_color_map.get(label, ['#e0e7ff', '#6366f1']))
        wc = WordCloud(
            width=640, height=340,
            background_color='white',
            colormap=cmap,
            max_words=100,
            prefer_horizontal=0.8,
            contour_width=1,
            contour_color='#e2e8f0'
        ).generate(text)
        fig_wc, ax = plt.subplots(figsize=(6.4, 3.4))
        fig_wc.patch.set_facecolor('white')
        ax.set_facecolor('white')
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"☁️ {label}", color='#1e293b', fontsize=13, pad=10, fontweight='bold')
        with wc_cols[i]:
            st.pyplot(fig_wc, use_container_width=True)

# =====================================
# ROW 5 — HISTOGRAM + BOX
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
        nbins=40, barmode='overlay', opacity=0.75,
        title='Distribusi Panjang Karakter',
        labels={'text_length': 'Jumlah Karakter', 'sentiment_label': 'Sentimen'}
    )
    fig_hist.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=14,
        xaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        legend=dict(orientation='h', yanchor='top', y=1.15),
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
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
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
        box=True, points='outliers',
        title='Distribusi Panjang Karakter (Violin)',
        labels={'text_length': 'Panjang Karakter', 'sentiment_label': 'Sentimen'}
    )
    fig_vio.update_layout(
        paper_bgcolor=PLOTLY_THEME['paper_bgcolor'],
        plot_bgcolor=PLOTLY_THEME['plot_bgcolor'],
        font_color=PLOTLY_THEME['font_color'],
        title_font_size=14,
        showlegend=False,
        xaxis=dict(gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(gridcolor=PLOTLY_THEME['gridcolor']),
        margin=dict(t=50, b=30)
    )
    st.plotly_chart(fig_vio, use_container_width=True)

# =====================================
# RINGKASAN STATISTIK
# =====================================
st.markdown('<div class="section-header">📊 Ringkasan Statistik per Sentimen</div>', unsafe_allow_html=True)

stats_cols = st.columns(3)
for i, (label, color) in enumerate(COLORS.items()):
    subset = filtered_df[filtered_df['sentiment_label'] == label]
    avg_len   = round(subset['text_length'].mean(), 1) if len(subset) else 0
    avg_words = round(subset['word_count'].mean(), 1)  if len(subset) else 0
    max_len   = int(subset['text_length'].max()) if len(subset) else 0
    with stats_cols[i]:
        st.markdown(f"""
        <div class="stats-card" style="--accent:{color}">
            <div class="stats-title" style="color:{color}">{label}</div>
            <div class="stats-row">
                📝 Rata-rata karakter &nbsp;→&nbsp; <span class="stats-val">{avg_len}</span><br>
                📖 Rata-rata kata &nbsp;→&nbsp; <span class="stats-val">{avg_words}</span><br>
                📏 Terpanjang &nbsp;→&nbsp; <span class="stats-val">{max_len} karakter</span><br>
                🔢 Total komentar &nbsp;→&nbsp; <span class="stats-val">{len(subset):,}</span>
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
    "<div class='footer'>Dashboard Analisis Sentimen WFH ASN · Dibuat dengan ❤️ menggunakan Streamlit & Plotly 🚀</div>",
    unsafe_allow_html=True
)
