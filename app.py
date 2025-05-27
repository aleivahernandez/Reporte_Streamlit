import streamlit as st
import pandas as pd
import re
from transformers import MarianMTModel, MarianTokenizer

st.set_page_config(page_title="Landing Page de Patentes Apícolas", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("ORBIT_REGISTRO_QUERY.csv")
    # Limpiar título: quitar texto en paréntesis
    df['Titulo_limpio'] = df['Title'].apply(lambda x: re.sub(r'\s*\([^)]*\)\s*', '', x).strip())
    return df

@st.cache_resource
def load_translation_model():
    model_name = "Helsinki-NLP/opus-mt-en-es"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def traducir_texto(texto, tokenizer, model):
    if not texto or len(texto.strip()) < 5:
        return "Resumen no disponible."
    inputs = tokenizer(texto, return_tensors="pt", truncation=True)
    translated = model.generate(**inputs, max_new_tokens=300)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

def traducir_titulo(titulo, tokenizer, model):
    # Traducir título completo (puedes simplificar si es muy largo)
    return traducir_texto(titulo, tokenizer, model)

# Cargar datos y modelo
df = load_data()
tokenizer, model = load_translation_model()

# Traducir títulos y crear lista para mostrar
# IMPORTANTE: para no traducir en cada reload, cacheamos el resultado en una nueva columna
if 'Titulo_es' not in df.columns:
    df['Titulo_es'] = df['Titulo_limpio'].apply(lambda t: traducir_titulo(t, tokenizer, model))

# Crear lista de patentes para mostrar en tarjetas, con índice para URL
patentes = []
for i, row in df.iterrows():
    patentes.append({"idx": i, "titulo": row['Titulo_es']})

# CSS para tarjetas
page_style = """
<style>
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill,minmax(280px,1fr));
    gap: 20px;
    padding: 10px;
  }
  .card {
    background: #e0f7fa;
    border-radius: 12px;
    padding: 20px;
    height: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    font-weight: 600;
    font-size: 1rem;
    color: #00796b;
  }
  .card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.2);
  }
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

# Mostrar grid de tarjetas
cards_html = '<div class="grid-container">'
for patente in patentes:
    cards_html += f"""
    <div class="card" onclick="window.location.href='/?idx={patente['idx']}'" role="button" tabindex="0">
        {patente['titulo']}
    </div>
    """
cards_html += '</div>'

st.markdown(cards_html, unsafe_allow_html=True)

# Leer parámetro idx para mostrar detalle
query_params = st.experimental_get_query_params()
if "idx" in query_params:
    try:
        idx = int(query_params["idx"][0])
        if 0 <= idx < len(df):
            row = df.iloc[idx]
