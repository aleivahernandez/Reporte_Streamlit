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
st.markdown(page_style, unsafe_allow_html=True)

def mostrar_landing():
    st.title("📋 Lista de Patentes Apícolas")
    st.markdown("Haz clic en una tarjeta para ver detalles.\n")

    tarjetas_html = '<div class="grid-container">'
    for idx, titulo in enumerate(st.session_state.titulos_traducidos):
        tarjetas_html += f'''
        <div class="card" onclick="window.location.href='/?idx={idx}'" role="button" tabindex="0">
            {titulo}
        </div>
        '''
    tarjetas_html += '</div>'
    st.markdown(tarjetas_html, unsafe_allow_html=True)

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
        st.experimental_set_query_params(idx=None)
        st.session_state.patente_seleccionada = None
        st.experimental_rerun()

# Obtener parámetros con st.query_params
query_params = st.query_params
if "idx" in query_params and query_params["idx"]:
    try:
        idx = int(query_params["idx"][0])
        mostrar_detalle(idx)
    except:
        mostrar_landing()
else:
    mostrar_landing()
