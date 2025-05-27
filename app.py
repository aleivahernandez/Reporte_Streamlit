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
    except Exception as e:
        return f"Error en traducción: {e}"

def limpiar_titulo(titulo):
    return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()

df = load_data()
df['Titulo_limpio'] = df['Title'].apply(limpiar_titulo)
df['Titulo_traducido'] = df['Titulo_limpio'].apply(traducir_texto)

st.sidebar.header("🎛️ Filtro por título de patente")
titulo_seleccionado = st.sidebar.selectbox("Selecciona un título", sorted(df['Titulo_limpio'].unique()))

df_filtrado = df[df['Titulo_limpio'] == titulo_seleccionado]

for _, row in df_filtrado.iterrows():
    st.subheader(row['Titulo_limpio'])
    st.markdown(f"*Título traducido:* {row['Titulo_traducido']}")
    resumen_traducido = traducir_texto(row['Abstract'])
    st.markdown(f"**Resumen en español (traducido automáticamente):** {resumen_traducido}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")
    st.markdown("---")
