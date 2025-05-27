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

# Traducir títulos *una sola vez* y guardar en sesión para no repetir traducción en cada ejecución
if "titulos_traducidos" not in st.session_state:
    st.session_state.titulos_traducidos = [traducir_texto(t) for t in df['Titulo_limpio']]

# Estado para patente seleccionada
if "patente_seleccionada" not in st.session_state:
    st.session_state.patente_seleccionada = None

def mostrar_landing():
    st.title("📋 Lista de Patentes Apícolas")
    st.markdown("Haz clic en un título para ver detalles.\n")

    # Mostrar en columnas para diseño tipo cards
    num_cols = 3
    cols = st.columns(num_cols)

    for i, (titulo, idx) in enumerate(zip(st.session_state.titulos_traducidos, df.index)):
        with cols[i % num_cols]:
            if st.button(titulo, key=f"btn_{idx}"):
                st.session_state.patente_seleccionada = idx

def mostrar_detalle(idx):
    row = df.loc[idx]
    st.title(st.session_state.titulos_traducidos[idx])
    resumen_traducido = traducir_texto(row['Abstract'])
    st.markdown(f"**Resumen en español:** {resumen_traducido}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")

    if st.button("← Volver al listado"):
        st.session_state.patente_seleccionada = None

if st.session_state.patente_seleccionada is None:
    mostrar_landing()
else:
    mostrar_detalle(st.session_state.patente_seleccionada)
