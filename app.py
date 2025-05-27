import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# Cargar datos
df = pd.read_csv("ORBIT_REGISTRO_QUERY.csv")

# Limpiar títulos
df['Titulo_limpio'] = df['Title'].fillna("").astype(str).apply(lambda x: x.strip())

# Traducir títulos si no están traducidos
@st.cache_data
def traducir_texto(texto):
    if not isinstance(texto, str) or len(texto.strip()) < 5:
        return "Título no disponible"
    try:
        return GoogleTranslator(source='en', target='es').translate(texto)
    except:
        return texto

@st.cache_data
def traducir_columna(col):
    return [traducir_texto(x) for x in col]

if 'Titulo_es' not in df.columns:
    df['Titulo_es'] = traducir_columna(df['Titulo_limpio'])

# Obtener parámetros de URL
query_params = st.query_params
idx = int(query_params.get("idx", [0])[0])

# Estilos
st.markdown("""
    <style>
    .tarjeta {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-radius: 0.5rem;
        transition: all 0.2s ease-in-out;
    }
    .tarjeta:hover {
        background-color: #e9ecef;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar detalle si hay idx
if idx:
    st.title("Detalle de Patente")
    patente = df.iloc[idx]
    st.subheader(patente['Titulo_es'])
    st.write(patente.get('Abstract', 'Resumen no disponible'))
    if st.button("🔙 Volver"):
        st.query_params.clear()
        st.rerun()


else:
    st.title("Informe de Patentes Apícolas")

    for i, row in df.iterrows():
        with st.container():
            if st.button(row['Titulo_es'], key=f"patente_{i}"):
                st.query_params["idx"] = i
                st.rerun()
