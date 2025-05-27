import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import re

# ==== Funciones de limpieza y traducción ====
def limpiar_titulo(titulo):
    if isinstance(titulo, str):
        return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()
    return ""

def traducir_texto(texto, src="en", dest="es"):
    if not isinstance(texto, str) or len(texto.strip()) < 5:
        return "Resumen no disponible."
    try:
        return GoogleTranslator(source=src, target=dest).translate(texto)
    except Exception:
        return "Traducción no disponible."

@st.cache_data(show_spinner=False)
def traducir_columna(textos):
    return [traducir_texto(t) for t in textos]

# ==== Carga de datos ====
df = pd.read_csv("datos_patentes.csv")  # Asegúrate que el nombre sea correcto

df["Titulo_limpio"] = df["Title"].apply(limpiar_titulo)
df["Titulo_es"] = traducir_columna(df["Titulo_limpio"])
df["Resumen_es"] = traducir_columna(df["Abstract"])

# ==== Estilos CSS ====
page_style = """
<style>
    body {
        background-color: #f0f2f6;
    }
    .card {
        background-color: white;
        padding: 20px;
        margin: 10px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        transition: 0.3s;
        cursor: pointer;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .card:hover {
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        transform: scale(1.02);
    }
    .cards-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# ==== Navegación por parámetros ====
params = st.query_params
idx = params.get("idx", [None])[0]
try:
    idx = int(idx) if idx is not None else None
except ValueError:
    idx = None

# ==== Página de detalle ====
if idx is not None and 0 <= idx < len(df):
    patente = df.iloc[idx]
    st.markdown("### 📝 Detalle de la patente")
    st.markdown(f"**Título:** {patente['Titulo_es']}")
    st.markdown(f"**Resumen:** {patente['Resumen_es']}")
    if st.button("🔙 Volver al listado"):
        st.query_params.clear()
        st.rerun()
else:
    # ==== Página de inicio (Landing Page) ====
    st.title("🌼 Informe de Patentes Apícolas")

    st.markdown('<div class="cards-container">', unsafe_allow_html=True)
    for i, row in df.iterrows():
        st.markdown(
            f"""
            <div class="card" onclick="window.location.href='/?idx={i}'" role="button" tabindex="0">
                {row['Titulo_es']}
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
