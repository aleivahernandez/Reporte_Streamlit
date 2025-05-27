import streamlit as st
import pandas as pd

# Cargar archivo
@st.cache_data
def load_data():
    return pd.read_csv("patentes_apicola.csv")

df = load_data()

# Título principal
st.title("📘 Informe de Patentes Apícolas")
st.markdown("Exploración visual e interactiva de las patentes relacionadas con la industria apícola.")

# Filtro por país
paises = df['Assignee country'].dropna().unique()
pais_seleccionado = st.sidebar.selectbox("Selecciona país", sorted(paises))
df_filtrado = df[df['Assignee country'] == pais_seleccionado]

# Sección de títulos
st.header("📌 Títulos de patentes")
for i, row in df_filtrado.iterrows():
    st.subheader(row['Title'])
    st.markdown(f"**Resumen:** {row['Abstract']}")
    st.markdown(f"**Inventores:** {row['Inventors']}")
    st.markdown(f"**Fecha prioridad:** {row['Earliest priority date']}")
    st.markdown("---")

# Estadísticas
st.header("📊 Estadísticas generales")
st.markdown("Distribución de publicaciones por país")
st.bar_chart(df['Assignee country'].value_counts())

# Fechas importantes
st.header("🕓 Evolución temporal")
df['Publication dates'] = pd.to_datetime(df['Publication dates'], errors='coerce')
st.line_chart(df['Publication dates'].dt.year.value_counts().sort_index())

# Información por código de país y estado
st.header("🌐 Códigos de país y estado")
st.dataframe(df[['Country code and status', 'Title']].dropna())

