import streamlit as st

st.set_page_config(
    page_title="Laboratorio Virtual de Electromagnetismo",
    page_icon="⚡",
    layout="wide"
)

st.sidebar.image(
    "https://raw.githubusercontent.com/Jmontoyaor/Computational-electromagnetics/main/Imagenes/Propela_logo.png",
    use_container_width=True
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

    .stApp {
        background-color: #0e1a40; /* Fondo de la app */
        color: #E0E0E0; /* Texto principal */
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3 {
        color: #00BFFF; /* Títulos */
        font-family: 'Poppins', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background-color: #222f5b !important; /* Sidebar */
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
    }

    section[data-testid="stSidebar"] * {
        color: #c6e2ff !important; /* Texto del sidebar */
    }
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)

# --- Title ---
st.title("Laboratorio Virtual de Electromagnetismo: Un Espacio Interactivo de Aprendizaje")
# --- Introduction ---
st.markdown("""
Bienvenido al **Laboratorio Virtual de Electromagnetismo**, un entorno interactivo diseñado para explorar de manera práctica los fenómenos electromagnéticos
a través de simulaciones computacionales y recursos didácticos.

Este proyecto busca integrar el rigor matemático con la experimentación digital, permitiendo que el estudiante
no solo realice cálculos, sino que también comprenda a fondo los principios que rigen el comportamiento del campo eléctrico y magnético en diversas aplicaciones.
""")

# Imagen centrada con descripción
col1, col2, col3 = st.columns([1, 2, 1])  # proporción para centrar
with col2:
    st.image(
        "https://github.com/Jmontoyaor/Computational-electromagnetics/blob/main/Imagenes/Background%20(2).png?raw=true",
        use_container_width=True,
        caption="Ilustración conceptual de un campo electromagnético"
    )


st.write("---")

# --- Features ---
st.header("¿Qué encontrarás en este laboratorio?")
st.markdown("""
-  **Simulaciones Interactivas:** Modifica parámetros como carga, corriente o geometría y observa en tiempo real cómo cambian los campos eléctricos y magnéticos.

-  **Cálculos Numéricos Asistidos:** Incluye métodos de resolución integral y diferencial para el análisis de cargas, campos y potenciales.

-  **Fundamento Teórico:** Cada módulo se basa en el libro *Electromagnetismo Computacional* del profesor **Julio César García Álvarez**, conectando la teoría con la práctica.

-  **Ejercicios Guiados:** Encuentra ejemplos aplicados y problemas que fortalecen el aprendizaje mediante el uso de herramientas computacionales.
""")

st.write("---")

# --- Reference ---
st.header("Bibliografía y Repositorio")
st.markdown("""
El material de apoyo y los ejercicios fueron basados en el libro:
**Julio César García Álvarez – Electromagnetismo Computacional**

Este libro está disponible en el repositorio institucional de la **Universidad Nacional de Colombia** en el siguiente enlace:
[Repositorio UNAL - Electromagnetismo Computacional](https://bffrepositorio.unal.edu.co/server/api/core/bitstreams/6cf02436-f3f9-4df7-9291-f990a388c846/content)
""")


st.write("---")

# --- Credits ---
st.header("Créditos")
st.markdown("""
Desarrollador: **Juan Fernando Montoya Ortiz**""")
st.markdown(" Asistente virtual: **ChatGPT (OpenAI)**, colaborando en la estructuración y organización del laboratorio virtual.")
