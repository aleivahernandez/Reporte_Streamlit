import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import re

st.set_page_config(page_title="Informe de Patentes Apícolas", layout="wide")

# ===== Estilos CSS personalizados =====
# Mantendremos los estilos, pero las tarjetas no usarán la funcionalidad onclick
page_style = """
<style>
body {
    background-color: #f9f4ef;
}
.card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 16px;
    margin: 12px;
    width: 300px;
    height: 120px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
    /* Eliminamos cursor: pointer y cualquier JS */
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    text-align: center;
}
.container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}
</style>
"""
st.markdown(page_style, unsafe_allow_html=True)

# ===== Funciones =====
def limpiar_titulo(titulo):
    if pd.isna(titulo):
        return ""
    return re.sub(r'\s*\([^)]*\)\s*', '', titulo).strip()

def traducir_texto(texto, src="en", dest="es"):
    if not isinstance(texto, str) or len(texto.strip()) < 5:
        return "Contenido no disponible o demasiado corto para traducir."
    try:
        return GoogleTranslator(source=src, target=dest).translate(texto)
    except Exception as e:
        st.warning(f"Error de traducción para el texto: '{texto[:50]}...' - {e}")
        return "Error de traducción."

@st.cache_data(show_spinner=False)
def cargar_y_preparar_datos(filepath):
    df = pd.read_csv(filepath)
    df["Titulo_limpio"] = df["Title"].apply(limpiar_titulo)

    st.info("Traduciendo títulos al español... Esto puede tomar un momento.")
    df["Titulo_es"] = [traducir_texto(t) for t in df["Titulo_limpio"]]

    st.info("Traduciendo resúmenes al español... Esto puede tomar un momento.")
    df["Resumen_es"] = [traducir_texto(t) for t in df["Abstract"]]

    return df

# ===== Cargar y preparar datos =====
df = cargar_y_preparar_datos("ORBIT_REGISTRO_QUERY.csv")


# ===== Landing page o vista detallada =====
query_params = st.query_params

if "idx" in query_params:
    try:
        idx = int(query_params["idx"][0])
        if 0 <= idx < len(df):
            patente = df.iloc[idx]
            st.title(patente["Titulo_es"])
            st.markdown(f"**Resumen:** {patente.get('Resumen_es', 'Resumen no disponible.')}")
            st.markdown("---")
            if st.button("🔙 Volver"):
                query_params.clear()
                st.rerun()
        else:
            st.error("Índice de patente no válido.")
            if st.button("🔙 Volver a la página principal"):
                query_params.clear()
                st.rerun()
    except ValueError:
        st.error("El índice proporcionado no es un número válido.")
        if st.button("🔙 Volver a la página principal"):
            query_params.clear()
            st.rerun()
    except Exception as e:
        st.error(f"Error al cargar la patente seleccionada: {e}")
        st.exception(e)
        if st.button("🔙 Volver a la página principal"):
            query_params.clear()
            st.rerun()
else:
    st.title("Informe de Patentes Apícolas - Landing Page")
    st.markdown("Haz clic en una patente para ver más detalles.")
    st.markdown('<div class="container">', unsafe_allow_html=True)

    # REEMPLAZO CLAVE AQUÍ: Usamos st.link_button en lugar del HTML con onclick
    # Cada link_button se mostrará como un botón en el layout.
    for i, titulo in enumerate(df["Titulo_es"]):
        # Puedes intentar aplicar tus estilos CSS a los botones con st.button/st.link_button
        # usando la key 'class', pero esto es limitado y experimental.
        # Lo más sencillo es simplemente aceptar el estilo por defecto del botón
        # o buscar alternativas más avanzadas si necesitas el estilo exacto de tarjeta.
        st.link_button(
            label=titulo,
            url=f"/?idx={i}",
            help=f"Ver detalles de: {titulo}"
        )
    st.markdown('</div>', unsafe_allow_html=True)
