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
        traduccion = GoogleTranslator(source='en', target='es').translate(texto)
        return traduccion
    except Exception:
        return "Error en traducción."

def limpiar_titulo(titulo):
    return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()

df = load_data()
df['Titulo_limpio'] = df['Title'].apply(limpiar_titulo)
df['Titulo_traducido'] = df['Titulo_limpio'].apply(traducir_texto)

# Inicializar variable de sesión
if "patente_seleccionada" not in st.session_state:
    st.session_state.patente_seleccionada = None

if st.session_state.patente_seleccionada is None:
    st.title("📋 Lista de Patentes Apícolas")
    st.markdown("Haz clic en un título para ver detalles.")

    # Mostrar títulos como botones
    for idx, row in df.iterrows():
        if st.button(row['Titulo_traducido'], key=f"btn_{idx}"):
            st.session_state.patente_seleccionada = idx
            # No usar st.experimental_rerun()
            st.experimental_rerun()
else:
    # Mostrar botón para volver
    if st.button("← Volver al listado"):
        st.session_state.patente_seleccionada = None
        st.experimental_rerun()

    # Mostrar detalle
    row = df.loc[st.session_state.patente_seleccionada]

    st.title(row['Titulo_traducido'])
    resumen_traducido = traducir_texto(row['Abstract'])
    st.markdown(f"**Resumen en español:** {resumen_traducido}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")
