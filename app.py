import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

st.set_page_config(page_title="Informe Patentes Apícolas", layout="wide")

# Leer datos
df = pd.read_csv("ORBIT_REGISTRO_QUERY.csv")

# Traducción con caché
@st.cache_data(show_spinner=False)
def traducir_texto(texto):
    if not isinstance(texto, str) or len(texto.strip()) < 5:
        return "Resumen no disponible."
    try:
        return GoogleTranslator(source='en', target='es').translate(texto)
    except:
        return "Error de traducción."

@st.cache_data(show_spinner=False)
def traducir_columna(col):
    return [traducir_texto(t) for t in col]

# Añadir columnas traducidas si no están
if 'Titulo_es' not in df.columns:
    df['Titulo_es'] = traducir_columna(df['Titulo_limpio'])
if 'Resumen_es' not in df.columns:
    df['Resumen_es'] = traducir_columna(df['Abstract'])

# Obtener índice desde URL
query_params = st.query_params
idx = query_params.get("idx", [None])[0]

# Estilo
st.markdown("""
<style>
.card-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}
.card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    flex: 1 1 calc(33.33% - 1rem);
    min-width: 250px;
    cursor: pointer;
    transition: transform 0.2s ease;
    text-decoration: none;
    color: inherit;
}
.card:hover {
    transform: scale(1.02);
    background-color: #e0e4ec;
}
</style>
""", unsafe_allow_html=True)

# Página de detalles
if idx is not None and idx.isdigit():
    i = int(idx)
    patente = df.iloc[i]
    st.markdown("### 🔙 [Volver al listado](/)")
    st.title(patente['Titulo_es'])
    st.markdown(f"**Resumen:** {patente['Resumen_es']}")
    st.markdown("---")
    st.dataframe(patente.to_frame().T)
else:
    st.title("🧠 Informe de Patentes Apícolas")
    st.markdown("Explora las invenciones registradas sobre la miel y sus aplicaciones.")
    st.markdown('<div class="card-container">', unsafe_allow_html=True)

    for i, row in df.iterrows():
        link = f"/?idx={i}"
        st.markdown(f"""
        <a href="{link}" class="card">
            {row['Titulo_es']}
        </a>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
