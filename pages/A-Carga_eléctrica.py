
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math


st.sidebar.image(
    "https://raw.githubusercontent.com/Jmontoyaor/Computational-electromagnetics/main/Imagenes/Propela_logo.png",
    use_container_width=True
)
# --- Estilos CSS Personalizados ---
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

    /* --- INICIO DE LA CORRECCIÓN --- */
    
    /* Esta es la nueva regla que soluciona el problema */
    label {
        color: #E0E0E0 !important; /* Asegura que el texto de los sliders sea visible */
    }

    /* Contenedor principal del expander */
    [data-testid="stExpander"] {
        border: 1px solid #00BFFF !important; /* Borde azul brillante */
        border-radius: 10px;
        background-color: #1c2a59; /* Fondo para el contenido interno */
    }

    /* El encabezado del expander (la parte que estaba blanca) */
    [data-testid="stExpander"] summary {
        background-color: #222f5b !important; /* Fondo del encabezado */
        color: #E0E0E0 !important; /* Color del texto del título */
        border-radius: 10px; /* Redondear esquinas */
    }
    
    section[data-testid="stSidebar"] {
        background-color: #222f5b;
        border-radius: 10px;
    }
    
    section[data-testid="stSidebar"] * {
        color: #c6e2ff !important;
    }

    /* Asegurar que el texto del título sea del color correcto */
    [data-testid="stExpander"] summary p {
        color: #E0E0E0 !important;
    }

    /* --- FIN DE LA CORRECCIÓN --- */

</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)


# Se crea una disposición de 2 columnas para la imagen y el título
# Se ajustó la proporción para dar más espacio a la imagen
col_img, col_title = st.columns([0.3, 1])

with col_img:
    # URL corregida para mostrar la imagen directamente desde GitHub
    st.image("https://raw.githubusercontent.com/Jmontoyaor/Computational-electromagnetics/main/Imagenes/Carga_Electrica.png", width=150)

with col_title:
    st.title("Carga Eléctrica")

# --- TEXTO CORREGIDO ---
# Texto actualizado y relevante para el tema de la carga eléctrica
st.markdown("#### Explora cómo se calcula las distancias de las particulas.")

st.write("---")


# --- Sección Teórica: Definición ---
st.header("Sección Teórica - Definición")
st.markdown("""
La carga eléctrica es una propiedad intrínseca de la materia que se manifiesta en fenómenos eléctricos y magnéticos.
Se presenta en dos tipos: **positiva** y **negativa**, asociadas respectivamente al protón y al electrón.

Su unidad de medida en el Sistema Internacional es el **coulomb (C)**, definido como la cantidad de carga que circula en un segundo por un conductor cuando la corriente es de un amperio.
Un coulomb equivale aproximadamente a **6.242 × 10¹⁸ electrones**, mientras que la carga elemental de un electrón es de **–1.602 × 10⁻¹⁹ C**, valor establecido experimentalmente por Robert A. Millikan en 1910.

En electromagnetismo se emplean las letras **Q** y **q** para representar la cantidad de carga eléctrica.
Estas variables permiten describir interacciones entre partículas y constituyen la base para las leyes fundamentales, como la **Ley de Coulomb** y el **campo eléctrico**.

El análisis de partículas cargadas requiere definir su posición en un sistema de coordenadas.
Los más empleados son:

- **Sistema cartesiano (x, y, z):** describe posiciones en un plano o en un espacio tridimensional.
- **Sistema geográfico (latitud, longitud):** utilizado en mapas y superficies terrestres.
- **Sistema esférico (r, φ, θ):** fundamental en física y astronomía, pues describe posiciones mediante una distancia radial y dos ángulos.

Estos marcos de referencia permiten estudiar trayectorias, posiciones y movimientos de partículas cargadas en distintos contextos físicos.
""")

col1, col2, col3 = st.columns([1, 2, 1])  # Proporción para centrar la imagen
with col2:
    st.image(
        # Esta es la nueva URL de la imagen de los planos
        "https://github.com/Jmontoyaor/Computational-electromagnetics/blob/main/Imagenes/Planos.png?raw=true",
        use_container_width=True,
        # Pie de foto actualizado para la nueva imagen
        caption="Ilustración de los planos de coordenadas"
    )


with st.expander("Ver Enunciado del Ejercicio 2.1 - Distancias entre Partículas", expanded=True):
    st.subheader("Enunciado del Problema")
    st.markdown("""
    Tres partículas A, B y C se encuentran ubicadas en el plano cartesiano en las siguientes coordenadas (expresadas en metros):
    - **Partícula A:** (2, 1.5) m
    - **Partícula B:** (-3, 1.5) m
    - **Partícula C:** (-2, -3) m

    **Se solicita:**
    a) Ubicar gráficamente los tres puntos en el plano de coordenadas XY.

    b) Calcular las distancias entre todos los pares de partículas utilizando la fórmula de distancia euclidiana:
    """)
    st.latex(r"d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}")
    st.markdown("""
    Específicamente calcule:
    - Distancia entre A y B ($d_{AB}$)
    - Distancia entre A y C ($d_{AC}$)
    - Distancia entre B y C ($d_{BC}$)

    c) Elaborar un segundo gráfico que muestre las distancias como segmentos de línea.

    d) Mostrar todos los cálculos paso a paso.

    e) Presentar los resultados finales en metros con dos decimales.
    """)

# (El código anterior: CSS, Título y Sección Teórica permanece igual)
# ...

# --- PARÁMETROS DE ENTRADA (AHORA EN LA PÁGINA PRINCIPAL) ---
st.header("Parámetros de Entrada")
st.markdown("Define las coordenadas para cada punto usando los sliders.")

# Crear tres columnas para los controles
col_a, col_b, col_c = st.columns(3)

# Entradas para el Punto A en la primera columna
with col_a:
    st.subheader("Punto A")
    ax_coord = st.slider('Coordenada X de A', min_value=-10.0,
                         max_value=10.0, value=2.0, step=0.1, format="%.2f", key="ax")
    ay_coord = st.slider('Coordenada Y de A', min_value=-10.0,
                         max_value=10.0, value=1.5, step=0.1, format="%.2f", key="ay")
A = (ax_coord, ay_coord)

# Entradas para el Punto B en la segunda columna
with col_b:
    st.subheader("Punto B")
    bx_coord = st.slider('Coordenada X de B', min_value=-10.0,
                         max_value=10.0, value=-3.0, step=0.1, format="%.2f", key="bx")
    by_coord = st.slider('Coordenada Y de B', min_value=-10.0,
                         max_value=10.0, value=1.5, step=0.1, format="%.2f", key="by")
B = (bx_coord, by_coord)

# Entradas para el Punto C en la tercera columna
with col_c:
    st.subheader("Punto C")
    cx_coord = st.slider('Coordenada X de C', min_value=-10.0,
                         max_value=10.0, value=-2.0, step=0.1, format="%.2f", key="cx")
    cy_coord = st.slider('Coordenada Y de C', min_value=-10.0,
                         max_value=10.0, value=-3.0, step=0.1, format="%.2f", key="cy")
C = (cx_coord, cy_coord)


# --- CÁLCULOS ---
# (El resto del código: Cálculos, Visualización, etc. permanece igual)
# ...
# --- CÁLCULOS ---
# Función para calcular la distancia euclidiana
def calcular_distancia(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)


# Calcular distancias
dist_AB = calcular_distancia(A, B)
dist_AC = calcular_distancia(A, C)
dist_BC = calcular_distancia(B, C)

# --- VISUALIZACIÓN GRÁFICA ---
st.header("📊 Visualización Gráfica")
col1, col2 = st.columns(2)

# Determinar límites dinámicos para los gráficos para que siempre se vean bien
all_x = [A[0], B[0], C[0], 0]
all_y = [A[1], B[1], C[1], 0]
x_min, x_max = min(all_x) - 1, max(all_x) + 1
y_min, y_max = min(all_y) - 1, max(all_y) + 1

# Gráfico 1: Ubicación de puntos
with col1:
    st.subheader("a. Ubicación de puntos")
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='k', linewidth=0.8)
    ax1.axvline(x=0, color='k', linewidth=0.8)

    # Plotear y anotar puntos
    for point, name in [(A, 'A'), (B, 'B'), (C, 'C')]:
        ax1.plot(point[0], point[1], 'ro', markersize=6)
        ax1.annotate(f'{name}=({point[0]:.2f}, {point[1]:.2f})', xy=point, xytext=(
            point[0] + 0.1, point[1] + 0.1), fontsize=9, color='red')
        ax1.plot([point[0], point[0]], [0, point[1]],
                 'k--', alpha=0.5, linewidth=0.8)
        ax1.plot([0, point[0]], [point[1], point[1]],
                 'k--', alpha=0.5, linewidth=0.8)

    ax1.set_xlabel('Eje X')
    ax1.set_ylabel('Eje Y')
    ax1.set_title('Ubicación en el Plano Cartesiano')
    st.pyplot(fig1)

# Gráfico 2: Trazo de distancias
with col2:
    st.subheader("b. Trazo de distancias")
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(y_min, y_max)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='k', linewidth=0.8)
    ax2.axvline(x=0, color='k', linewidth=0.8)

    # Plotear puntos y anotar
    for point, name in [(A, 'A'), (B, 'B'), (C, 'C')]:
        ax2.plot(point[0], point[1], 'ro', markersize=6)
        ax2.annotate(f'{name}=({point[0]:.2f}, {point[1]:.2f})', xy=point, xytext=(
            point[0] + 0.1, point[1] + 0.1), fontsize=9, color='red')

    # Dibujar las líneas de distancia
    ax2.plot([A[0], B[0]], [A[1], B[1]], 'b-',
             linewidth=2, label=f'AB = {dist_AB:.2f}')
    ax2.plot([A[0], C[0]], [A[1], C[1]], 'g-',
             linewidth=2, label=f'AC = {dist_AC:.2f}')
    ax2.plot([B[0], C[0]], [B[1], C[1]], 'm-',
             linewidth=2, label=f'BC = {dist_BC:.2f}')
    ax2.legend()

    ax2.set_xlabel('Eje X')
    ax2.set_ylabel('Eje Y')
    ax2.set_title('Distancias entre Puntos')
    st.pyplot(fig2)

# --- CÁLCULOS DETALLADOS ---
st.header("Cálculos de Distancias")
st.markdown("A continuación se muestra el cálculo paso a paso para cada distancia, utilizando la fórmula de la distancia euclidiana:")
st.latex(r"d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}")

with st.expander("Distancia AB"):
    st.latex(
        fr"d(A,B) = \sqrt{{({B[0]:.2f} - {A[0]:.2f})^2 + ({B[1]:.2f} - {A[1]:.2f})^2}}")
    st.latex(
        fr"d(A,B) = \sqrt{{({B[0] - A[0]:.2f})^2 + ({B[1] - A[1]:.2f})^2}}")
    st.latex(
        fr"d(A,B) = \sqrt{{{(B[0] - A[0])**2:.2f} + {(B[1] - A[1])**2:.2f} }}")
    st.latex(fr"d(A,B) = \sqrt{{{(B[0] - A[0])**2 + (B[1] - A[1])**2:.2f} }}")
    st.success(f"**Distancia AB = {dist_AB:.2f}**")

with st.expander("Distancia AC"):
    st.latex(
        fr"d(A,C) = \sqrt{{({C[0]:.2f} - {A[0]:.2f})^2 + ({C[1]:.2f} - {A[1]:.2f})^2}}")
    st.latex(
        fr"d(A,C) = \sqrt{{({C[0] - A[0]:.2f})^2 + ({C[1] - A[1]:.2f})^2}}")
    st.latex(
        fr"d(A,C) = \sqrt{{{(C[0] - A[0])**2:.2f} + {(C[1] - A[1])**2:.2f} }}")
    st.latex(fr"d(A,C) = \sqrt{{{(C[0] - A[0])**2 + (C[1] - A[1])**2:.2f} }}")
    st.success(f"**Distancia AC = {dist_AC:.2f}**")

with st.expander("Distancia BC"):
    st.latex(
        fr"d(B,C) = \sqrt{{({C[0]:.2f} - {B[0]:.2f})^2 + ({C[1]:.2f} - {B[1]:.2f})^2}}")
    st.latex(
        fr"d(B,C) = \sqrt{{({C[0] - B[0]:.2f})^2 + ({C[1] - B[1]:.2f})^2}}")
    st.latex(
        fr"d(B,C) = \sqrt{{{(C[0] - B[0])**2:.2f} + {(C[1] - B[1])**2:.2f} }}")
    st.latex(fr"d(B,C) = \sqrt{{{(C[0] - B[0])**2 + (C[1] - B[1])**2:.2f} }}")
    st.success(f"**Distancia BC = {dist_BC:.2f}**")

st.info(
    """
    **Este ejercicio demuestra:**
    1.  La ubicación de puntos en el plano cartesiano.
    2.  El cálculo de distancias entre puntos usando la fórmula euclidiana.
    3.  La visualización gráfica de las distancias como segmentos de línea.
    """
)
