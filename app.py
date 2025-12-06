import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go   # grafik interaktif

# =========================
# Fungsi Model & Euler
# =========================
def model_gdp_solow(Y, t, r, K):
    """
    Model Pertumbuhan Solow (sederhana / logistik satu variabel):
    dY/dt = r * Y * (1 - Y/K)
    """
    return r * Y * (1.0 - Y / K)

def euler_method(func, y0, t_points, params):
    """
    Metode Euler manual.
    func     : fungsi turunan f(t, y)
    y0       : nilai awal
    t_points : array waktu
    params   : parameter tambahan (mis. (r, K))
    """
    y = np.zeros(len(t_points))
    y[0] = y0
    h = t_points[1] - t_points[0]

    for i in range(len(t_points) - 1):
        slope = func(y[i], t_points[i], *params)
        y[i+1] = y[i] + h * slope

    return y

def estimate_r(t_data, gdp_values):
    """
    Estimasi r dari data dengan regresi:
    ln(Y) = a t + b, dimana a ≈ r
    """
    logY = np.log(gdp_values)
    r_est, b_est = np.polyfit(t_data, logY, 1)
    return r_est

# =========================
# Layout Streamlit
# =========================
st.set_page_config(layout="wide")
st.markdown(
    """
    <h1 style='white-space: nowrap;'>
        Simulasi Pertumbuhan Ekonomi (Model Pertumbuhan Solow Sederhana) dengan Metode Euler
    </h1>
    """,
    unsafe_allow_html=True
)

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_gdp():
    df = pd.read_csv("GDP.csv")
    return df

df = load_gdp()

# Deteksi kolom nama negara
if "Country Name" in df.columns:
    country_col = "Country Name"
elif "Country" in df.columns:
    country_col = "Country"
else:
    st.error("Kolom nama negara tidak ditemukan di GDP.csv")
    st.stop()

countries = sorted(df[country_col].unique())

# =========================
# PILIH NEGARA (dengan placeholder)
# =========================
country = st.selectbox(
    "Pilih Negara",
    ["-- Pilih Negara --"] + countries,
    index=0,
)

# =========================
# SIDEBAR – HANYA SATU HEADER DI AWAL
# =========================
st.sidebar.header("Pengaturan Data & Parameter")

# =========================
# JIKA NEGARA BELUM DIPILIH → HANYA INFO
# =========================
if country == "-- Pilih Negara --":
    st.info("Silakan pilih negara terlebih dahulu di dropdown di atas untuk memunculkan pengaturan dan grafik.")
else:
    # =========================
    # AMBIL DATA NEGARA YANG DIPILIH
    # =========================
    row_country = df[df[country_col] == country].iloc[0]

    # Ambil kolom tahun yang valid (bisa di-cast ke int)
    year_cols = []
    for col in df.columns:
        try:
            int(col)
            year_cols.append(col)
        except:
            pass

    years = np.array([int(y) for y in year_cols])
    gdp_values = row_country[year_cols].values.astype(float)

    # Buang NaN
    mask_valid = ~np.isnan(gdp_values)
    years = years[mask_valid]
    gdp_values = gdp_values[mask_valid]

    # =========================
    # SIDEBAR – RENTANG TAHUN (di bawah "Pengaturan Data & Parameter")
    # =========================
    year_min = int(years[0])
    year_max = int(years[-1])

    start_year, end_year = st.sidebar.select_slider(
        "Rentang Tahun Data",
        options=list(range(year_min, year_max + 1)),
        value=(year_min, year_max),
    )

    mask_range = (years >= start_year) & (years <= end_year)
    years_range = years[mask_range]
    gdp_range = gdp_values[mask_range]

    # Time index t
    t_data = np.arange(len(gdp_range))

    # Estimasi r default dari data
    r_default = float(estimate_r(t_data, gdp_range))

    # Estimasi K default
    K_default = float(1.5 * np.max(gdp_range))
    K_min = float(1.05 * np.max(gdp_range))
    K_max = float(3.0 * np.max(gdp_range))

    # =========================
    # SIDEBAR – HEADER PARAMETER MODEL SETELAH RENTANG TAHUN
    # =========================
    st.sidebar.header("Parameter Model Solow (Sederhana)")

    # SLIDER PARAMETER MODEL
    r = st.sidebar.slider(
        "Laju Pertumbuhan r (per tahun)",
        min_value=0.00,
        max_value=0.20,
        value=float(np.clip(r_default, 0.0, 0.2)),
        step=0.005,
    )

    K = st.sidebar.slider(
        "Kapasitas Jangka Panjang K (steady-state GDP)",
        min_value=K_min,
        max_value=K_max,
        value=K_default,
        step=(K_max - K_min) / 100.0,
    )

    h = st.sidebar.slider(
        "Step Size h (tahun)",
        min_value=0.1,
        max_value=1.0,
        value=1.0,
        step=0.1,
    )

    # =========================
    # SIMULASI EULER (SOLOW)
    # =========================
    t_start = 0.0
    t_end = float(len(gdp_range) - 1)
    t_sim = np.arange(t_start, t_end + h, h)

    Y0 = gdp_range[0]
    Y_euler_sim = euler_method(model_gdp_solow, Y0, t_sim, (r, K))
    Y_euler_at_years = np.interp(t_data, t_sim, Y_euler_sim)

    mse = float(np.mean((gdp_range - Y_euler_at_years) ** 2))

    # =========================
    # GRAFIK INTERAKTIF
    # =========================
    st.subheader(f"Data GDP vs Simulasi Euler (Model Solow) – {country}")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years_range,
        y=gdp_range,
        mode="lines+markers",
        name="Data Asli GDP",
        line=dict(color="blue"),
        marker=dict(color="blue"),
    ))

    fig.add_trace(go.Scatter(
        x=years_range,
        y=Y_euler_at_years,
        mode="lines+markers",
        name="Simulasi Euler (Solow)",
        line=dict(color="orange"),
        marker=dict(color="orange"),
    ))

    fig.update_layout(
        xaxis_title="Tahun",
        yaxis_title="GDP",
        title=f"Pertumbuhan GDP {country} – Model Pertumbuhan Solow (Sederhana)",
        autosize=False,
        width=900,
        height=500,
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # METRIK ERROR
    # =========================
    st.markdown(f"<h3><b>Mean Squared Error (MSE):  {mse:,.2f}</b></h3>", unsafe_allow_html=True)

    # =========================
    # PENJELASAN MODEL
    # =========================
    st.markdown(r"Model yang digunakan")
    st.latex(r"\frac{dY}{dt} = r\,Y\left(1 - \frac{Y}{K}\right)")

    st.markdown(
        """
        **Dengan:**

        - **r** : laju pertumbuhan GDP (per tahun)  
        - **K** : kapasitas jangka panjang / steady-state GDP  
        - **h** : step size metode Euler  

        Geser slider untuk melihat bagaimana perubahan parameter memengaruhi hasil simulasi.
        """
    )
