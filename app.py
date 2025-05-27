import streamlit as st
import pandas as pd

st.set_page_config(page_title="Informe de Patentes Apícolas", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("patentes_apicola.csv")

df = load_data()

st.title("🐝 Informe de Patentes en la Industria Apícola")
st.markdown("Una exploración visual de las patentes apícolas.")

# Filtro por TÍTULO
st.sidebar.header("🎛️ Filtro por título de patente")
titulos = df['Title'].dropna().unique()
titulo_seleccionado = st.sidebar.selectbox("Selecciona un título", sorted(titulos))

df_filtrado = df[df['Title'] == titulo_seleccionado]

# Mostrar la información de la patente seleccionada
for _, row in df_filtrado.iterrows():
    st.subheader(row['Title'])
    st.markdown(f"**Resumen:** {row['Abstract']}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Asignatario(s):** {row['Latest standardized assignees - inventors removed']}")
    st.markdown(f"**País del asignatario:** {row['Assignee country']}")
    st.markdown(f"**Dirección del asignatario:** {row['Assignee address']}")
    st.markdown(f"**Fecha de prioridad más antigua:** {row['Earliest priority date']}")
    st.markdown(f"**Número de publicación:** {row['Publication numbers with kind code']}")
    st.markdown(f"**Código de país y estado:** {row['Country code and status']}")
    st.markdown(f"**Fecha de publicación:** {row['Publication dates']}")
    st.markdown("---")
