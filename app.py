import streamlit as st
import pandas as pd
import re
from googletrans import Translator

st.set_page_config(page_title="Informe de Patentes Apícolas", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ORBIT_REGISTRO_QUERY.csv")

translator = Translator()

def traducir_texto(texto):
    if not texto or len(texto.strip()) < 5:
        return "Resumen no disponible."
    try:
        traduccion = translator.translate(texto, src='en', dest='es')
        return traduccion.text
    except Exception as e:
        return f"Error en traducción: {e}"

def limpiar_titulo(titulo):
    # Elimina todo lo que esté entre paréntesis (inclusive los paréntesis) y espacios alrededor
    return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()

# Cargar datos
df = load_data()

# Preprocesar títulos
df['Titulo_limpio'] = df['Title'].apply(limpiar_titulo)

# Sidebar
st.sidebar.header("🎛️ Filtro por título de patente")
titulo_seleccionado = st.sidebar.selectbox("Selecciona un título", sorted(df['Titulo_limpio'].unique()))

# Filtrar
df_filtrado = df[df['Titulo_limpio'] == titulo_seleccionado]

# Mostrar resultados
for _, row in df_filtrado.iterrows():
    st.subheader(row['Titulo_limpio'])
    resumen_traducido = traducir_texto(row['Abstract'])
    st.markdown(f"**Resumen en español (traducido automáticamente):** {resumen_traducido}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")
    st.markdown("---")


