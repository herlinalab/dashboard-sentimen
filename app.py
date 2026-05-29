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
# CUSTOM CSS
# =====================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

    .stApp {
        background-color: #f0f4ff;
        background-image: radial-gradient(#c7d2fe 1px, transparent 1px);
        background-size: 28px 28px;
        min-height: 100vh;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6366f1 0%, #818cf8 100%) !important;
        border-right: none;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.3) !important; }

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
        content: ''; position: absolute;
        top: -60px; right: -60px;
        width: 280px; height: 280px;
        background: rgba(255,255,255,0.1); border-radius: 50%;
    }
    .hero-container::after {
        content: ''; position: absolute;
        bottom: -80px; left: 30%;
        width: 220px; height: 220px;
        background: rgba(255,255,255,0.07); border-radius: 50%;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.25);
        border: 1px solid rgba(255,255,255,0.4);
        color: #fff; padding: 0.25rem 0.9rem;
        border-radius: 20px; font-size: 0.72rem;
        font-weight: 700; letter-spacing: 0.1em;
        text-transform: uppercase; margin-bottom: 0.9rem;
    }
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2rem; font-weight: 800;
        color: #fff; margin: 0 0 0.5rem 0;
        line-height: 1.25; text-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 0.95rem; font-weight: 500; margin: 0;
    }

    .metric-card {
        background: #fff; border-radius: 18px;
        padding: 1.5rem 1.2rem; text-align: center;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07);
        border-top: 5px solid var(--accent);
        transition: transform 0.2s, box-shadow 0.2s;
        position: relative; overflow: hidden;
    }
    .metric-card:hover { transform: translateY(-4px); box-shadow: 0 10px 32px rgba(0,0,0,0.12); }
    .metric-card-bg {
        position: absolute; top: -20px; right: -20px;
        width: 80px; height: 80px;
        border-radius: 50%; background: var(--accent); opacity: 0.08;
    }
    .metric-icon { font-size: 2.2rem; margin-bottom: 0.4rem; }
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 2.6rem; font-weight: 800;
        color: #1e293b; line-height: 1; margin-bottom: 0.25rem;
    }
    .metric-label {
        color: #64748b; font-size: 0.8rem;
        font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;
    }
    .metric-pct {
        font-size: 0.85rem; font-weight: 700; margin-top: 0.3rem;
        padding: 0.15rem 0.6rem; border-radius: 10px; display: inline-block;
        background: rgba(0,0,0,0.05);
    }

    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.15rem; font-weight: 800; color: #1e293b;
        display: flex; align-items: center; gap: 0.5rem;
        margin: 2rem 0 0.5rem 0;
        padding: 0.7rem 1.2rem;
        background: #fff; border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 4px solid #6366f1;
    }

    /* Interpretasi box — dinamis */
    .interp-box {
        border-radius: 12px;
        padding: 1rem 1.4rem;
        font-size: 0.875rem;
        line-height: 1.75;
        color: #334155;
        margin-bottom: 1rem;
        border-left: 4px solid var(--icolor);
        background: var(--ibg);
    }
    .interp-label {
        font-weight: 800; font-size: 0.72rem;
        text-transform: uppercase; letter-spacing: 0.1em;
        color: var(--icolor); margin-bottom: 0.35rem;
    }

    .insight-box {
        background: linear-gradient(135deg, #eff6ff, #faf5ff);
        border: 2px solid #e0e7ff; border-radius: 14px;
        padding: 1.2rem 1.5rem; color: #334155;
        font-size: 0.9rem; line-height: 1.7;
        box-shadow: 0 2px 12px rgba(99,102,241,0.1);
    }
    .insight-title {
        font-weight: 800; color: #6366f1;
        font-size: 0.75rem; text-transform: uppercase;
        letter-spacing: 0.1em; margin-bottom: 0.5rem;
    }

    .stats-card {
        background: #fff; border-radius: 16px;
        padding: 1.3rem 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        border-bottom: 4px solid var(--accent);
    }
    .stats-title { font-weight: 800; font-size: 1rem; margin-bottom: 0.8rem; }
    .stats-row { font-size: 0.82rem; color: #64748b; line-height: 2; }
    .stats-val { color: #1e293b; font-weight: 700; }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; font-weight: 700 !important;
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

    hr { border-color: #e2e8f0 !important; }
    div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
    .footer { text-align: center; color: #94a3b8; font-size: 0.82rem; padding: 1rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# =====================================
# HELPER — interpretasi box
# =====================================
def interp(color, bg, title, text):
    return f"""
    <div class="interp-box" style="--icolor:{color}; --ibg:{bg}">
        <div class="interp-label">📝 {title}</div>
        {text}
    </div>
    """

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    df = pd.read_csv("hasil_sentimen.csv")
    df['sentiment_label'] = df['sentiment'].map({1: 'Positif', 0: 'Negatif', 2: 'Netral'})
    return df

df = load_data()

COLORS = {'Positif': '#10b981', 'Negatif': '#f43f5e', 'Netral': '#f59e0b'}
PT = {'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': '#fafafa',
      'font_color': '#334155', 'gridcolor': '#e2e8f0'}

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
    st.markdown("<small>Analisis sentimen komentar Instagram terkait kebijakan WFH ASN di hari Jumat.</small>",
                unsafe_allow_html=True)
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
positif = (filtered_df['sentiment'] == 1).sum()
negatif = (filtered_df['sentiment'] == 0).sum()
netral  = (filtered_df['sentiment'] == 2).sum()
pct_pos = round(positif / total_data * 100, 1) if total_data else 0
pct_neg = round(negatif / total_data * 100, 1) if total_data else 0
pct_net = round(netral  / total_data * 100, 1) if total_data else 0

c1, c2, c3, c4 = st.columns(4)
for col, icon, val, label, pct, color in [
    (c1, "📦", total_data, "Total Komentar", "100%",        "#6366f1"),
    (c2, "😊", positif,    "Positif",         f"{pct_pos}%", "#10b981"),
    (c3, "😠", negatif,    "Negatif",         f"{pct_neg}%", "#f43f5e"),
    (c4, "😶", netral,     "Netral",          f"{pct_net}%", "#f59e0b"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card" style="--accent:{color}">
            <div class="metric-card-bg"></div>
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{val:,}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-pct" style="color:{color}">{pct}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# SECTION 1 — DISTRIBUSI SENTIMEN
# =====================================
st.markdown('<div class="section-header">📈 Distribusi Sentimen</div>', unsafe_allow_html=True)

sentiment_count = filtered_df['sentiment_label'].value_counts().reset_index()
sentiment_count.columns = ['Sentimen', 'Jumlah']

# Tentukan sentimen dominan secara dinamis
dom = sentiment_count.iloc[0]['Sentimen']
dom_n = sentiment_count.iloc[0]['Jumlah']
dom_pct = round(dom_n / total_data * 100, 1) if total_data else 0
min_s = sentiment_count.iloc[-1]['Sentimen']
min_n = sentiment_count.iloc[-1]['Jumlah']
min_pct = round(min_n / total_data * 100, 1) if total_data else 0

dom_color = COLORS.get(dom, '#6366f1')
dom_bg = {'Positif': '#f0fdf4', 'Negatif': '#fff1f2', 'Netral': '#fffbeb'}.get(dom, '#eff6ff')

col_r1a, col_r1b = st.columns(2)

with col_r1a:
    fig_bar = px.bar(
        sentiment_count, x='Sentimen', y='Jumlah',
        color='Sentimen', color_discrete_map=COLORS,
        text='Jumlah', title='Jumlah Komentar per Sentimen'
    )
    fig_bar.update_traces(textposition='outside', textfont_size=14, marker_line_width=0)
    fig_bar.update_layout(
        paper_bgcolor=PT['paper_bgcolor'], plot_bgcolor=PT['plot_bgcolor'],
        font_color=PT['font_color'], showlegend=False, title_font_size=15,
        xaxis=dict(gridcolor=PT['gridcolor'], showgrid=False),
        yaxis=dict(gridcolor=PT['gridcolor']),
        margin=dict(t=50, b=30), bargap=0.3
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_r1b:
    fig_pie = px.pie(
        sentiment_count, values='Jumlah', names='Sentimen',
        color='Sentimen', color_discrete_map=COLORS,
        title='Proporsi Sentimen (%)', hole=0.55
    )
    fig_pie.update_traces(
        textinfo='percent+label', pull=[0.05, 0.05, 0.05],
        hovertemplate='<b>%{label}</b><br>%{value} komentar<br>%{percent}<extra></extra>'
    )
    fig_pie.update_layout(
        paper_bgcolor=PT['paper_bgcolor'], font_color=PT['font_color'],
        title_font_size=15, showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.15),
        margin=dict(t=50, b=30)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Interpretasi Distribusi
st.markdown(interp(
    dom_color, dom_bg,
    "Interpretasi Distribusi Sentimen",
    f"Dari total <b>{total_data:,}</b> komentar yang dianalisis, sentimen <b style='color:{dom_color}'>{dom}</b> "
    f"mendominasi dengan <b>{dom_n:,} komentar ({dom_pct}%)</b>. "
    f"Hal ini menunjukkan bahwa sebagian besar masyarakat merespons kebijakan WFH ASN di hari Jumat secara <b>{dom.lower()}</b>. "
    f"Sementara itu, sentimen <b>{min_s}</b> menjadi yang paling sedikit muncul dengan hanya <b>{min_n:,} komentar ({min_pct}%)</b>, "
    f"menandakan respons tersebut relatif jarang diekspresikan oleh publik."
), unsafe_allow_html=True)

# =====================================
# SECTION 2 — SENTIMENT SCORE GAUGE
# =====================================
st.markdown('<div class="section-header">🎯 Sentiment Score</div>', unsafe_allow_html=True)

score = round((positif - negatif) / total_data * 100, 1) if total_data else 0
score_color = "#10b981" if score > 0 else "#f43f5e" if score < 0 else "#f59e0b"
score_bg    = "#f0fdf4" if score > 0 else "#fff1f2" if score < 0 else "#fffbeb"

col_g1, col_g2 = st.columns([1, 1])

with col_g1:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        delta={'reference': 0, 'valueformat': '.1f'},
        title={'text': "Sentiment Score", 'font': {'size': 15, 'color': '#334155'}},
        number={'suffix': '', 'font': {'size': 40, 'color': '#1e293b'}},
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
            'bgcolor': 'white', 'bordercolor': '#e2e8f0',
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor=PT['paper_bgcolor'], font_color=PT['font_color'],
        margin=dict(t=60, b=20, l=30, r=30), height=300
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_g2:
    arah = "cenderung <b style='color:#10b981'>POSITIF</b>" if score > 10 \
           else "cenderung <b style='color:#f43f5e'>NEGATIF</b>" if score < -10 \
           else "<b style='color:#f59e0b'>NETRAL / BERIMBANG</b>"
    kuat = "kuat" if abs(score) > 40 else "moderat" if abs(score) > 15 else "lemah"
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(interp(
        score_color, score_bg,
        "Interpretasi Sentiment Score",
        f"Sentiment Score dihitung dari selisih komentar Positif dan Negatif dibagi total data, "
        f"menghasilkan nilai <b style='color:{score_color}'>{score:+.1f}</b> pada skala −100 hingga +100. "
        f"Nilai ini menunjukkan bahwa opini publik secara keseluruhan {arah} dengan intensitas yang <b>{kuat}</b>. "
        f"<br><br>Angka mendekati <b>+100</b> berarti dukungan sangat kuat, sedangkan mendekati <b>−100</b> "
        f"berarti penolakan sangat kuat terhadap kebijakan WFH ASN."
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# SECTION 3 — TOP KEYWORDS
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

kw_scales = {
    'Positif': ['#d1fae5', '#10b981'],
    'Negatif': ['#ffe4e6', '#f43f5e'],
    'Netral':  ['#fef3c7', '#f59e0b'],
}
kw_bg = {'Positif': '#f0fdf4', 'Negatif': '#fff1f2', 'Netral': '#fffbeb'}

col_r3a, col_r3b, col_r3c = st.columns(3)
kw_results = {}

for label, col in [('Positif', col_r3a), ('Netral', col_r3b), ('Negatif', col_r3c)]:
    subset = filtered_df[filtered_df['sentiment_label'] == label]['clean_text']
    if len(subset) > 0:
        top_words = get_top_words(subset, n=10)
        kw_results[label] = top_words
        if top_words:
            words_df = pd.DataFrame(top_words, columns=['Kata', 'Frekuensi'])
            fig_kw = px.bar(
                words_df, x='Frekuensi', y='Kata',
                orientation='h',
                color='Frekuensi',
                color_continuous_scale=kw_scales[label],
                title=f'Top 10 Kata — {label}',
                text='Frekuensi'
            )
            fig_kw.update_traces(textposition='outside', marker_line_width=0)
            fig_kw.update_layout(
                paper_bgcolor=PT['paper_bgcolor'], plot_bgcolor=PT['plot_bgcolor'],
                font_color=PT['font_color'], title_font_size=14,
                showlegend=False, coloraxis_showscale=False,
                xaxis=dict(gridcolor=PT['gridcolor']),
                yaxis=dict(autorange='reversed', gridcolor='rgba(0,0,0,0)'),
                margin=dict(t=50, b=10, l=10, r=30), height=340
            )
            with col:
                st.plotly_chart(fig_kw, use_container_width=True)
    else:
        with col:
            st.info(f"Tidak ada data {label}")

# Interpretasi Top Keywords — per sentimen
col_i3a, col_i3b, col_i3c = st.columns(3)
for label, col in [('Positif', col_i3a), ('Netral', col_i3b), ('Negatif', col_i3c)]:
    top = kw_results.get(label, [])
    if top:
        k1 = top[0][0]; k2 = top[1][0] if len(top) > 1 else '-'; k3 = top[2][0] if len(top) > 2 else '-'
        kw_color = COLORS[label]
        kw_bg_c  = kw_bg[label]

        if label == 'Positif':
            narasi = (f'Kata-kata dominan seperti <b>"{k1}"</b>, <b>"{k2}"</b>, dan <b>"{k3}"</b> '
                      f"mencerminkan ekspresi dukungan dan apresiasi masyarakat terhadap kebijakan WFH ASN. "
                      f"Kehadiran kata-kata ini mengindikasikan bahwa sebagian publik melihat kebijakan ini "
                      f"sebagai langkah yang menguntungkan dan patut disambut baik.")
        elif label == 'Negatif':
            narasi = (f'Kata-kata seperti <b>"{k1}"</b>, <b>"{k2}"</b>, dan <b>"{k3}"</b> '
                      f"muncul paling sering dalam komentar bernada negatif. "
                      f"Ini mengindikasikan kekhawatiran atau ketidaksetujuan publik, kemungkinan terkait "
                      f"efektivitas layanan ASN, produktivitas, atau dampak WFH terhadap kinerja pemerintah.")
        else:
            narasi = (f'Pada komentar netral, kata <b>"{k1}"</b>, <b>"{k2}"</b>, dan <b>"{k3}"</b> '
                      f"paling sering muncul. Komentar netral umumnya berisi pertanyaan, pernyataan fakta, "
                      f"atau observasi tanpa opini yang jelas — menunjukkan sebagian publik masih "
                      f"bersikap wait-and-see terhadap kebijakan ini.")

        with col:
            st.markdown(interp(kw_color, kw_bg_c, f"Interpretasi Kata Kunci {label}", narasi),
                        unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# SECTION 4 — WORD CLOUD
# =====================================
st.markdown('<div class="section-header">☁️ Word Cloud per Sentimen</div>', unsafe_allow_html=True)

wc_color_map = {
    'Positif': ['#a7f3d0', '#059669'],
    'Negatif': ['#fecdd3', '#e11d48'],
    'Netral':  ['#fde68a', '#d97706'],
}
wc_interp = {
    'Positif': ("Kata-kata berukuran besar pada word cloud ini mencerminkan tema yang paling sering "
                "diasosiasikan dengan dukungan publik. Semakin besar ukuran kata, semakin tinggi "
                "frekuensinya dalam komentar positif — menggambarkan inti narasi yang mendukung kebijakan."),
    'Negatif': ("Word cloud sentimen negatif memperlihatkan tema-tema yang memicu penolakan atau kritik. "
                "Perhatikan kata-kata dominan untuk memahami isu utama yang menjadi keberatan "
                "masyarakat terhadap kebijakan WFH ASN."),
    'Netral':  ("Word cloud netral menampilkan kosakata yang digunakan dalam komentar yang tidak "
                "memihak. Kata-kata ini cenderung bersifat deskriptif atau informatif, "
                "mencerminkan sikap publik yang masih menimbang kebijakan ini secara objektif."),
}

wc_cols = st.columns(len(selected_sentiment)) if selected_sentiment else []

for i, label in enumerate(selected_sentiment):
    subset = filtered_df[filtered_df['sentiment_label'] == label]['clean_text']
    text = " ".join(subset.astype(str))
    if text.strip():
        cmap = mcolors.LinearSegmentedColormap.from_list("wc", wc_color_map.get(label, ['#e0e7ff', '#6366f1']))
        wc = WordCloud(
            width=640, height=320,
            background_color='white', colormap=cmap,
            max_words=100, prefer_horizontal=0.8,
            contour_width=1, contour_color='#e2e8f0'
        ).generate(text)
        fig_wc, ax = plt.subplots(figsize=(6.4, 3.2))
        fig_wc.patch.set_facecolor('white')
        ax.set_facecolor('white')
        ax.imshow(wc, interpolation='bilinear')
        ax.axis("off")
        ax.set_title(f"☁️ Word Cloud — {label}", color='#1e293b', fontsize=12, pad=8, fontweight='bold')
        with wc_cols[i]:
            st.pyplot(fig_wc, use_container_width=True)

# Interpretasi Word Cloud — satu baris per sentimen yang dipilih
wc_interp_cols = st.columns(len(selected_sentiment)) if selected_sentiment else []
for i, label in enumerate(selected_sentiment):
    kw_c  = COLORS[label]
    kw_bg_c = kw_bg[label]
    with wc_interp_cols[i]:
        st.markdown(interp(kw_c, kw_bg_c, f"Interpretasi Word Cloud {label}", wc_interp[label]),
                    unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# SECTION 5 — RINGKASAN STATISTIK
# =====================================
filtered_df = filtered_df.copy()
filtered_df['text_length'] = filtered_df['clean_text'].astype(str).apply(len)
filtered_df['word_count']  = filtered_df['clean_text'].astype(str).apply(lambda x: len(x.split()))

st.markdown('<div class="section-header">📊 Ringkasan Statistik per Sentimen</div>', unsafe_allow_html=True)

stats_cols = st.columns(3)
stats_data = {}
for label, color in COLORS.items():
    subset = filtered_df[filtered_df['sentiment_label'] == label]
    avg_len   = round(subset['text_length'].mean(), 1) if len(subset) else 0
    avg_words = round(subset['word_count'].mean(), 1)  if len(subset) else 0
    max_len   = int(subset['text_length'].max()) if len(subset) else 0
    stats_data[label] = {'avg_len': avg_len, 'avg_words': avg_words, 'max_len': max_len, 'n': len(subset)}

for i, (label, color) in enumerate(COLORS.items()):
    d = stats_data[label]
    with stats_cols[i]:
        st.markdown(f"""
        <div class="stats-card" style="--accent:{color}">
            <div class="stats-title" style="color:{color}">{label}</div>
            <div class="stats-row">
                📝 Rata-rata karakter &nbsp;→&nbsp; <span class="stats-val">{d['avg_len']}</span><br>
                📖 Rata-rata kata &nbsp;→&nbsp; <span class="stats-val">{d['avg_words']}</span><br>
                📏 Terpanjang &nbsp;→&nbsp; <span class="stats-val">{d['max_len']} karakter</span><br>
                🔢 Total komentar &nbsp;→&nbsp; <span class="stats-val">{d['n']:,}</span>
            </div>
        </div>""", unsafe_allow_html=True)

# Interpretasi Statistik — gabungan
st.markdown("<br>", unsafe_allow_html=True)
# Cari sentimen dengan rata-rata kata terbanyak
max_words_label = max(stats_data, key=lambda x: stats_data[x]['avg_words'])
max_words_val   = stats_data[max_words_label]['avg_words']
min_words_label = min(stats_data, key=lambda x: stats_data[x]['avg_words'])
min_words_val   = stats_data[min_words_label]['avg_words']
mw_color = COLORS[max_words_label]

st.markdown(interp(
    mw_color, kw_bg.get(max_words_label, '#eff6ff'),
    "Interpretasi Ringkasan Statistik",
    f"Analisis panjang komentar menunjukkan bahwa komentar bernada <b style='color:{mw_color}'>{max_words_label}</b> "
    f"rata-rata menggunakan <b>{max_words_val} kata</b> — lebih panjang dibanding sentimen lainnya. "
    f"Hal ini mengindikasikan bahwa kelompok tersebut cenderung mengungkapkan pendapatnya secara lebih elaboratif dan detail. "
    f"Sebaliknya, komentar <b>{min_words_label}</b> rata-rata hanya <b>{min_words_val} kata</b>, "
    f"menunjukkan ekspresi yang lebih singkat dan langsung. "
    f"Perbedaan ini bisa mencerminkan tingkat keterlibatan emosional yang berbeda antar kelompok sentimen."
), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# SECTION 6 — DATASET & DOWNLOAD
# =====================================
st.markdown('<div class="section-header">🗂️ Dataset Hasil Analisis</div>', unsafe_allow_html=True)

display_cols = [c for c in ['clean_text', 'sentiment', 'sentiment_label'] if c in filtered_df.columns]
st.dataframe(filtered_df[display_cols].reset_index(drop=True), use_container_width=True, height=300)

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
