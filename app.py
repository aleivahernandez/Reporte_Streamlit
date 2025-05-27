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

if "patente_seleccionada" not in st.session_state:
    st.session_state.patente_seleccionada = None

# Estilos CSS para fondo y tarjetas
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

.card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 25px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.25);
}

h1 {
    text-align: center;
    margin-bottom: 2rem;
    font-weight: 700;
    color: #005f73;
}

button[role="button"] {
    all: unset;
    width: 100%;
    height: 100%;
    display: block;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

def mostrar_landing():
    st.title("📋 Lista de Patentes Apícolas")
    st.markdown("Haz clic en una tarjeta para ver detalles.\n")

    num_cols = 3
    cols = st.columns(num_cols)

    for i, (titulo, idx) in enumerate(zip(st.session_state.titulos_traducidos, df.index)):
        with cols[i % num_cols]:
            btn_key = f"btn_{idx}"
            # Botón estilizado para ocupar toda la tarjeta
            if st.button(titulo, key=btn_key):
                st.session_state.patente_seleccionada = idx
            # Aplica estilo de tarjeta al botón
            st.markdown(
                f"""
                <style>
                div.stButton > button#{btn_key} {{
                    all: unset;
                    cursor: pointer;
                    width: 100%;
                    height: 150px;
                    background: rgba(255,255,255,0);
                    border-radius: 15px;
                }}
                </style>
                """, unsafe_allow_html=True
            )
            # Se usa st.markdown para el fondo y texto porque el botón no admite estilos complejos directamente
            # El truco aquí es que el botón está invisible pero ocupa todo el espacio
            st.markdown(f'<div class="card">{titulo}</div>', unsafe_allow_html=True)

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
