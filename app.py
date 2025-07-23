# app.py

import streamlit as st
import datetime

from data_fetching import (
    get_inflacion, get_tasa_monetaria, get_reservas,
    get_tipo_cambio, get_cny, get_merval, get_cedears
)
from plotting import (
    plot_inflacion, plot_tasa_monetaria, plot_reservas,
    plot_tipo_cambio, plot_cny, plot_merval, plot_cedears
)

# Configurar la página
st.set_page_config(page_title="Monitor Financiero", layout="wide")


st.markdown("""
<style>
/* Fondo general */
.stApp {
    background-color: #1E90FF;
}

/* Cambiar fondo del encabezado */
[data-testid="stHeader"] {
    background-color: #1E90FF;
}

/* Quitar sombra */
[data-testid="stHeader"] div {
    box-shadow: none;
}
</style>
""", unsafe_allow_html=True)


# Función para aplicar estilos CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Aplicar el CSS
local_css("styles.css")

# --- Título ---
col_titulo, col_fecha1, col_fecha2 = st.columns([2.5, 1.2, 1.2])

with col_titulo:
    st.markdown("""
    <h1 style='color:white; text-transform: uppercase; margin-bottom: 0;'>
    MONITOR FINANCIERO
    </h1>
    <h5 style='color:white; font-weight: normal; margin-top: -20px;'>
    indicadores monetarios, cambiarios y bursátiles
    </h5>
    """, unsafe_allow_html=True)

with col_fecha1:
    start_date = st.date_input("Desde", value=datetime.date(2024,08,01), min_value=datetime.date(2023, 1, 1), max_value=datetime.date.today(), key="start")

with col_fecha2:
    end_date = st.date_input("Hasta", value=datetime.date.today(), min_value=start_date, max_value=datetime.date.today(), key="end")


# --- Cargar Datos ---
with st.spinner('Descargando datos...'):
    df_inflacion = get_inflacion(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df_tasa = get_tasa_monetaria(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df_reservas = get_reservas(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df_tc = get_tipo_cambio(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df_cny = get_cny(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df_merval = get_merval(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    df_cedears = get_cedears(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

# --- Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(plot_inflacion(df_inflacion), use_container_width=True)
    st.plotly_chart(plot_tasa_monetaria(df_tasa), use_container_width=True)

with col2:
    st.plotly_chart(plot_reservas(df_reservas), use_container_width=True)
    st.plotly_chart(plot_tipo_cambio(df_tc), use_container_width=True)
    st.plotly_chart(plot_cny(df_cny), use_container_width=True)

with col3:
    st.plotly_chart(plot_merval(df_merval), use_container_width=True)
    st.plotly_chart(plot_cedears(df_cedears), use_container_width=True)


# Footer
st.caption(f"Actualizado el {datetime.date.today().strftime('%d/%m/%Y')}")

