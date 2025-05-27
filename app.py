import streamlit as st
import pandas as pd
import re
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Informe de Patentes Apícolas", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ORBIT_REGISTRO_QUERY.csv")

def traducir_texto(texto):
    if not texto or len(texto.strip()) < 5:
        return "Resumen no disponible."
    try:
        return GoogleTranslator(source='en', target='es').translate(texto)
    except Exception:
        return "Error en traducción."

def limpiar_titulo(titulo):
    return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()

df = load_data()
df['Titulo_limpio'] = df['Title'].apply(limpiar_titulo)

if "titulos_traducidos" not in st.session_state:
    st.session_state.titulos_traducidos = [traducir_texto(t) for t in df['Titulo_limpio']]

page_style = """
<style>
body {
    background: linear-gradient(135deg, #c3e9f3, #eaf6f6);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
    padding: 1rem;
}
.main > div {
    max-width: 1100px;
    margin: auto;
}
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill,minmax(280px,1fr));
    gap: 20px;
}
.card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 20px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    user-select: none;
    font-weight: 600;
    font-size: 1.1rem;
    color: #005f73;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.25);
}
</style>
"""
st.markdown(page_style, un_
