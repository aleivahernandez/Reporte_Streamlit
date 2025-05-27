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
df['Titulo_traducido'] = df['Titulo_limpio'].apply(traducir_texto)

# Selector de título (solo títulos traducidos para mostrar)
titulo_traducido = st.selectbox("Selecciona una patente:", df['Titulo_traducido'].tolist())

# Mostrar detalles de la patente seleccionada
row = df[df['Titulo_traducido'] == titulo_traducido].iloc[0]

st.title(row['Titulo_traducido'])
resumen_traducido = traducir_texto(row['Abstract'])
st.markdown(f"**Resumen en español:** {resumen_traducido}")
st.markdown(f"**Inventores:** {row['Inventors']}")
st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
st.markdown(f"**País del asignatario:** {row['Assignee country']}")
st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")
