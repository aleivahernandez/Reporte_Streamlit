import streamlit as st
import pandas as pd
import re
from transformers import MarianMTModel, MarianTokenizer

st.set_page_config(page_title="Informe de Patentes Apícolas", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("ORBIT_REGISTRO_QUERY.csv")

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

def limpiar_titulo(titulo):
    return re.sub(r'^[A-Z]{2}\d+[A-Z]?\s*-\s*', '', titulo).strip()

# Cargar datos y modelo
df = load_data()
tokenizer, model = load_translation_model()

# Preprocesar títulos
df['Titulo_limpio'] = df['Title'].apply(limpiar_titulo)

# Sidebar
st.sidebar.header("🎛️ Filtro por título de patente")
titulo_seleccionado = st.sidebar.selectbox("Selecciona un título", sorted(df['Titulo_limpio'].unique()))

# Filtrar
df_filtrado = df[df['Titulo_limpio'] == titulo_seleccionado]

# Mostrar resultados
for _, row in df_filtrado.iterrows():
    st.subheader(row['Titulo_limpio'])
    resumen_traducido = traducir_texto(row['Abstract'], tokenizer, model)
    st.markdown(f"**Resumen en español (traducido automáticamente):** {resumen_traducido}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")
    st.markdown("---")

