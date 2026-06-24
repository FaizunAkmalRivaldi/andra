import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
import base64

# =====================================================
# KONFIGURASI HALAMAN
# =====================================================

st.set_page_config(
    page_title="Simulator What-If",
    page_icon="🌊",
    layout="wide"
)

# =====================================================
# FUNGSI BACKGROUND VIDEO
# =====================================================

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

video_path = "teholong.mp4"
video_base64 = get_base64_of_bin_file(video_path)

# =====================================================
# CSS CUSTOM
# =====================================================

video_html = f"""
<style>
    #myVideo {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        z-index: -1;
    }}
    .overlay {{
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%;
        min-height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: -1;
    }}
</style>
<div class="overlay"></div>
<video autoplay loop muted id="myVideo">
  <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
  Your browser does not support HTML5 video.
</video>
"""

st.markdown(video_html, unsafe_allow_html=True)

st.markdown("""
<style>
    /* Make all Streamlit containers transparent to show the video */
    .stApp {
        background: transparent;
    }
    .stApp > header {
        background-color: transparent;
    }
    .main .block-container {
        padding-top: 2rem; /* Add some space from the top */
        background-color: transparent;
    }

    /* Styling Judul - Tema Grand Blue */
    .big-title {
        text-align: center;
        color: #00BFFF; /* Deep Sky Blue */
        font-size: 48px;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000000;
    }
    .sub-title {
        text-align: center;
        color: #E0FFFF; /* Light Cyan */
        font-size: 20px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px #000000;
    }

    /* Styling untuk card dan elemen lainnya */
    div[data-testid="stMetric"],
    div[data-testid="stDataFrame"],
    div[data-testid="stPlotlyChart"],
    .st-emotion-cache-1r6slb0 { /* Container for recommendations */
        background-color: rgba(0, 70, 128, 0.75); /* Opacity ditingkatkan agar teks lebih terbaca */
        backdrop-filter: blur(10px); /* Efek kaca buram (frosted glass) */
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #00BFFF;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    /* Container khusus untuk rekomendasi */
    .recommendation-box {
        background-color: rgba(0, 70, 128, 0.75);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #00BFFF;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        color: white;
    }
    /* Menargetkan container yang kita buat secara manual */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"]:has(div.st-emotion-cache-1r6slb0) {
        padding-top: 20px !important; /* Menambah padding di dalam container rekomendasi */
    }

    /* Warna teks agar kontras */
    body, .stMetric, .stMarkdown, .stText {
        color: white;
    }
    .stMetric > div > div > div {
        color: white;
    }
    .st-ag, .st-c3, .st-c4 { /* For dataframes */
        color: white !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #002244; /* Dark Blue Solid */
    }
    div[data-testid="stSidebarUserContent"] {
        padding: 1rem; /* Menambah padding di dalam sidebar */
    }
    .st-emotion-cache-16txtl3 { /* Judul sidebar */
        color: white;
    }
    .st-emotion-cache-1y4p8pa, .st-emotion-cache-1kyxreq { /* Teks dan label slider di sidebar */
        color: white;
    }
    .st-emotion-cache-1v0mbdj { /* Ikon di sidebar */
        fill: white;
    }

    /* Menyembunyikan dekorasi default */
    #MainMenu {display: none;}
    footer {display: none;}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("model_keuntungan.pkl")

# =====================================================
# BASELINE
# =====================================================

baseline_input = np.array([[10, 10]])
baseline_pred = model.predict(baseline_input)[0]

# =====================================================
# FUNGSI SIMULASI
# =====================================================

def run_simulation(iklan, diskon):

    input_baru = np.array([[iklan, diskon]])

    prediksi = model.predict(input_baru)[0]

    delta = prediksi - baseline_pred

    return prediksi, delta

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class='big-title'>
🌊 Simulator Keuntungan
</div>

<div class='sub-title'>
Analisis What-If Berbasis Machine Learning
</div>
""", unsafe_allow_html=True)

st.divider()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Pengaturan variabel")

st.sidebar.markdown(
"""
Ubah nilai variabel berikut untuk melihat dampaknya terhadap keuntungan.
"""
)

iklan_slider = st.sidebar.slider(
    "📢 Anggaran Promosi (Juta)",
    min_value=0,
    max_value=50,
    value=10
)

diskon_slider = st.sidebar.slider(
    "🏷️ Diskon Oolong Tea (%)",
    min_value=0,
    max_value=50,
    value=10
)

# =====================================================
# JALANKAN SIMULASI
# =====================================================

hasil_pred, delta = run_simulation(
    iklan_slider,
    diskon_slider
)

# =====================================================
# KPI CARD
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="💰 Keuntungan Awal",
        value=f"Rp {baseline_pred:.2f} Jt"
    )

with col2:
    st.metric(
        label="📈 Prediksi Keuntungan Baru",
        value=f"Rp {hasil_pred:.2f} Jt"
    )

with col3:
    st.metric(
        label="🚀 Perubahan",
        value=f"{delta:.2f} Jt"
    )

st.divider()

# =====================================================
# REKOMENDASI
# =====================================================

st.subheader("📝 Kata Senior")

if delta > 20:
    message = f"Strategi ini sangat baik karena meningkatkan keuntungan sebesar {delta:.2f} juta."
elif delta > 0:
    message = f"Strategi memberikan peningkatan keuntungan sebesar {delta:.2f} juta."
elif delta == 0:
    message = "Tidak terdapat perubahan dibanding kondisi baseline."
else:
    message = f"Strategi menurunkan keuntungan sebesar {abs(delta):.2f} juta."

# Menampilkan pesan di dalam container HTML kustom
st.markdown(f'<div class="recommendation-box">{message}</div>', unsafe_allow_html=True)



# =====================================================
# DATAFRAME
# =====================================================

st.subheader("📊 Perbandingan Kondisi")

df = pd.DataFrame({
    "Kondisi": ["Awal", "Setelah Intervensi"],
    "Keuntungan (Jt)": [baseline_pred, hasil_pred]
})

st.dataframe(df, use_container_width=True)

# =====================================================
# BAR CHART
# =====================================================

fig_bar = px.bar(
    df,
    x="Kondisi",
    y="Keuntungan (Jt)",
    text="Keuntungan (Jt)",
    title="Perbandingan Keuntungan"
)

fig_bar.update_traces(
    texttemplate='%{text:.2f}',
    textposition='outside'
)

st.plotly_chart(
    fig_bar,
    use_container_width=True
)

# =====================================================
# GAUGE CHART
# =====================================================

st.subheader("🎯 Indikator Keuntungan")

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=hasil_pred,
        title={"text": "Prediksi Keuntungan"},
        gauge={
            "axis": {
                "range": [0, 200]
            }
        }
    )
)

st.plotly_chart(
    fig_gauge,
    use_container_width=True
)

# =====================================================
# DELTA CHART
# =====================================================

st.subheader("📉 Analisis Perubahan")

delta_df = pd.DataFrame({
    "Kategori": ["Delta"],
    "Nilai": [delta]
})

fig_delta = px.bar(
    delta_df,
    x="Kategori",
    y="Nilai",
    text="Nilai",
    title="Perubahan Keuntungan terhadap Baseline"
)

st.plotly_chart(
    fig_delta,
    use_container_width=True
)

# =====================================================
# SENSITIVITY ANALYSIS
# =====================================================

st.subheader("📈 Analisis Sensitivitas")

iklan_range = np.arange(0, 51)

prediksi_sens = []

for i in iklan_range:

    prediksi = model.predict([[i, diskon_slider]])[0]

    prediksi_sens.append(prediksi)

df_sens = pd.DataFrame({
    "Anggaran Promosi (Juta)": iklan_range,
    "Prediksi Keuntungan (Juta)": prediksi_sens
})

fig_sens = px.line(
    df_sens,
    x="Anggaran Promosi (Juta)",
    y="Prediksi Keuntungan (Juta)",
    markers=True,
    title="Peta Sensitivitas Anggaran Promosi"
)

st.plotly_chart(
    fig_sens,
    use_container_width=True
)

# =====================================================
# RINGKASAN AKHIR
# =====================================================

st.subheader("📋 Ringkasan Simulasi")

summary_text = f"""
**Keuntungan Awal:** Rp {baseline_pred:.2f} Juta <br>
**Prediksi Setelah Intervensi:** Rp {hasil_pred:.2f} Juta <br>
**Perubahan:** Rp {delta:.2f} Juta <br>
<hr>
Simulator ini membantu kita melihat bagaimana perubahan anggaran promosi dan diskon "Oolong Tea"
dapat mempengaruhi keuntungan. Gunakan ini untuk membuat keputusan yang lebih baik,
seperti yang diajarkan para senior di klub "Peek a Boo". <br>
*Cheers!*
"""

st.markdown(f'<div class="recommendation-box">{summary_text}</div>', unsafe_allow_html=True)