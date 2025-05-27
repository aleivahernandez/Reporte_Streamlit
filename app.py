import streamlit as st
import pandas as pd
import re
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Informe de Patentes Apícolas", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ORBIT_REGISTRO_QUERY.csv")

def limpiar_titulo(titulo):
    # Quitar paréntesis y espacios
    return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()

def traducir_texto(texto, src="en", dest="es"):
    if not texto or (isinstance(texto, float) and pd.isna(texto)):
        return "Resumen no disponible."
    texto_str = str(texto).strip()
    if len(texto_str) < 5:
        return "Resumen no disponible."
    try:
        return GoogleTranslator(source=src, target=dest).translate(texto_str)
    except Exception as e:
        return f"Error en traducción: {e}"


df = load_data()

# Limpiamos títulos y traducimos
df['Titulo_limpio'] = df['Title'].apply(limpiar_titulo)

# Traduce títulos y abstract una sola vez y cachea resultados
@st.cache_data(show_spinner=False)
def traducir_columna_texto(textos):
    return [traducir_texto(t) for t in textos]

df['Titulo_es'] = traducir_columna_texto(df['Titulo_limpio'])
df['Resumen_es'] = traducir_columna_texto(df['Abstract'])

# Landing page: Mostrar tarjetas con títulos traducidos
st.title("Informe de Patentes Apícolas - Landing Page")

st.write("Haz clic en una patente para ver más detalles.")

# Para la navegación, usamos query params para seleccionar índice
query_params = st.experimental_get_query_params()
idx_seleccionado = int(query_params.get("idx", [0])[0])

# Mostrar tarjetas
cols_per_row = 3
for i in range(0, len(df), cols_per_row):
    cols = st.columns(cols_per_row)
    for j, col in enumerate(cols):
        idx = i + j
        if idx >= len(df):
            break
        titulo = df.loc[idx, 'Titulo_es']
        # Tarjeta clicable: al hacer clic, cambia el query param idx
        card_html = f"""
        <div class="card" role="button" tabindex="0" 
             onclick="window.location.href='/?idx={idx}'" 
             style="padding: 15px; margin: 5px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    background: #f9f9f9; cursor: pointer; height: 120px; overflow: hidden;">
            <h4 style="font-size: 16px; color: #333;">{titulo}</h4>
        </div>
        """
        col.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# Mostrar detalle si se seleccionó índice válido
if 0 <= idx_seleccionado < len(df):
    row = df.iloc[idx_seleccionado]
    st.header(row['Titulo_es'])
    st.markdown(f"**Resumen:** {row['Resumen_es']}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")

