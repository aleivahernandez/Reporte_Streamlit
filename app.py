import streamlit as st
import pandas as pd
import re
from googletrans import Translator

st.set_page_config(page_title="Informe de Patentes Apícolas", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ORBIT_REGISTRO_QUERY.csv")

def limpiar_titulo(titulo):
    return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()

# Cargar datos
df = load_data()

# Limpiar títulos
df['Titulo_limpio'] = df['Title'].apply(limpiar_titulo)

translator = Translator()

def traducir_texto(texto):
    if not texto or len(texto.strip()) < 5:
        return "Resumen no disponible."
    try:
        resultado = translator.translate(texto, src='en', dest='es')
        return resultado.text
    except Exception as e:
        return "Error en traducción."

# Sidebar con lista de títulos limpios
st.sidebar.header("🎛️ Filtro por título de patente")
titulo_seleccionado = st.sidebar.selectbox("Selecciona un título", sorted(df['Titulo_limpio'].unique()))

# Filtrar DataFrame
df_filtrado = df[df['Titulo_limpio'] == titulo_seleccionado]

# Mostrar tarjeta con título traducido y resumen traducido
for _, row in df_filtrado.iterrows():
    st.subheader(row['Titulo_limpio'])
    resumen_traducido = traducir_texto(row['Abstract'])
    st.markdown(f"**Resumen en español (traducido):** {resumen_traducido}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")
    st.markdown("---")
