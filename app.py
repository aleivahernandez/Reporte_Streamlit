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

def mostrar_landing():
    st.title("📋 Lista de Patentes Apícolas")
    st.markdown("Haz clic en una tarjeta para ver detalles.\n")

    num_cols = 3
    cols = st.columns(num_cols)

    card_style = """
    <style>
    .card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        height: 150px;  /* altura fija */
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background-color: #fafafa;
        cursor: pointer;
        box-shadow: 2px 2px 5px rgb(0 0 0 / 0.1);
        transition: box-shadow 0.3s ease;
    }
    .card:hover {
        box-shadow: 4px 4px 15px rgb(0 0 0 / 0.2);
    }
    </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    for i, (titulo, idx) in enumerate(zip(st.session_state.titulos_traducidos, df.index)):
        with cols[i % num_cols]:
            # Generar un id único para el botón oculto
            btn_key = f"btn_{idx}"
            # Usar un botón invisible para capturar el clic
            if st.button("", key=btn_key, help="Ver detalles de la patente", args=None, kwargs=None):
                st.session_state.patente_seleccionada = idx

            # Mostrar la tarjeta como HTML (texto clicable no porque Streamlit no lo permite fácilmente,
            # pero el botón invisible encima captura clics)
            tarjeta_html = f"""
            <div class="card">
                <p style="font-weight:bold; font-size: 1.1rem; margin: 0;">{titulo}</p>
            </div>
            """
            st.markdown(tarjeta_html, unsafe_allow_html=True)

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
