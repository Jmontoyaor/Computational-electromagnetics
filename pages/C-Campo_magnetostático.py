
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# --- CONFIGURACIÓN DE LA BARRA LATERAL Y ESTILOS ---
st.set_page_config(layout="wide", page_title="Campo Eléctrico")

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

# --- ENCABEZADO DE LA PÁGINA ---
col_img, col_title = st.columns([0.2, 1])

with col_img:
    # URL actualizada a una imagen más relevante para el tema
    st.image("https://raw.githubusercontent.com/Jmontoyaor/Computational-electromagnetics/main/Imagenes/Campo.png", width=150)

with col_title:
    st.title("Campo Magnestostático")


# --- CUERPO TEÓRICO ---
st.header("Fundamentos Teóricos del Campo Magnetostático")

# 1. Concepto
with st.container():
    st.subheader("1. Concepto de Campo Magnetostático")
    st.markdown(r"""
    El **campo magnetostático** se origina cuando las **cargas eléctricas están en movimiento**,
    es decir, debido a corrientes eléctricas.  
    Fue descubierto por **Hans Christian Ørsted (1820)**, quien observó que una corriente
    eléctrica desviaba la aguja de una brújula.
    
    El campo magnético se representa con el vector **densidad de flujo magnético** $\vec{B}$,
    que es **perpendicular** a la corriente que lo genera.
    """)

# 2. Ley de Biot-Savart
with st.container():
    st.subheader("2. Ley de Biot-Savart")
    st.markdown(r"""
    Formulada por **Biot y Savart (1820)**, describe la contribución al campo magnético de
    un **elemento de corriente** en un punto del espacio:
    """)
    st.latex(
        r"d\vec{B} = \frac{\mu_0}{4\pi} \frac{ I \, d\vec{l} \times \hat{a}_R }{R^2}")
    st.markdown(r"""
    Donde:  
    - $\mu_0$ = permeabilidad magnética del vacío  
    - $I$ = corriente eléctrica  
    - $d\vec{l}$ = vector tangente al conductor  
    - $\hat{a}_R$ = vector unitario hacia el punto de observación  
    - $R$ = distancia al punto  
    
     Es análoga a la **ley de Coulomb** para el campo eléctrico, pero aplicada a corrientes.
    """)

# 3. Regla de la mano derecha
with st.container():
    st.subheader("3. Regla de la Mano Derecha")
    st.markdown(r"""
    La dirección del campo magnético $\vec{B}$ se obtiene con la **regla de la mano derecha**:  
    - Dedos → dirección de la corriente $I$  
    - Pulgar → dirección del campo magnético $\vec{B}$  
    """)

# 4. Campo total
with st.container():
    st.subheader("4. Campo Magnético Total")
    st.markdown(r"""
    Para obtener el campo en un punto se integra la contribución de todos los elementos de corriente:
    """)
    st.latex(
        r"\vec{B}(x,y,z) = \frac{\mu_0 I}{4\pi} \int_{L} \frac{ d\vec{l} \times \hat{a}_R }{R^2}")

# 5. Unidades
with st.container():
    st.subheader("5. Unidades del Campo Magnético")
    st.markdown(r"""
    - **Tesla (T)** = $\text{N} / (\text{A} \cdot \text{m})$
    - **Weber por metro cuadrado** ($\text{Wb/m}^2$)  
    - **Gauss (G)**, con $1 \, \text{T} = 10^4 \, \text{G}$  
    """)

# 6. Ejemplos
with st.container():
    st.subheader("6. Ejemplos Importantes")
    st.markdown(r"""
    - Cable conductor recto → el campo disminuye con la distancia  
    - Varios cables paralelos → se aplica superposición  
    - Espira circular → genera un campo en su eje  
    """)

# 7. Ley de Gauss
with st.container():
    st.subheader("7. Ley de Gauss para el Magnetismo")
    st.markdown(r"""
    Explica una propiedad fundamental del campo magnético:
    """)
    st.latex(r"\Phi_M = \iint_{S} \vec{B} \cdot d\vec{s} = 0")
    st.markdown(r"""
    Es decir:  
    - El flujo magnético neto a través de una superficie cerrada siempre es **cero**  
    - No existen monopolos magnéticos  
    - Las líneas de campo magnético son siempre **cerradas**, salen de un polo y entran en el otro  
    """)


st.title("Campo Magnético de un Conductor Infinito Desplazado")

st.markdown("""
Este simulador muestra el campo magnético **H** alrededor de un conductor infinito con corriente 
en la dirección **+z**.  
Ahora puedes mover el conductor en el plano XY y observar cómo cambia el campo.
""")

# --- Parámetros controlados por el usuario ---
I = st.slider("Corriente (A)", min_value=-10.0,
              max_value=10.0, value=5.0, step=1.0)
x0 = st.slider("Posición X del conductor", -5.0, 5.0, 0.0, 0.1)
y0 = st.slider("Posición Y del conductor", -5.0, 5.0, 0.0, 0.1)

plotlim = [-5, 5, -5, 5]

# --- Malla ---
dx = (plotlim[1] - plotlim[0]) / 20
dy = (plotlim[3] - plotlim[2]) / 20
xrange = np.arange(plotlim[0], plotlim[1] + dx, dx)
yrange = np.arange(plotlim[2], plotlim[3] + dy, dy)
X, Y = np.meshgrid(xrange, yrange)

# --- Distancia radial al nuevo centro ---
R = np.sqrt((X - x0)**2 + (Y - y0)**2)
R[R == 0] = np.nan  # evitar división por cero

# Vectores unitarios en dirección phi (-Δy, Δx)
phiX = -(Y - y0) / R
phiY = (X - x0) / R

# --- Campo magnético ---
H = I / (2 * np.pi * R)
U = H * phiX
V = H * phiY

# --- Graficar ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.quiver(X, Y, U, V, color="blue")
ax.set_aspect("equal")
ax.set_xlim(plotlim[0], plotlim[1])
ax.set_ylim(plotlim[2], plotlim[3])
ax.set_xlabel("X location (m)")
ax.set_ylabel("Y location (m)")
ax.set_title(
    f"Campo Magnético para I = {I:.1f} A, Conductor en ({x0:.1f}, {y0:.1f})")
ax.grid(True)

# Dibujar la posición del conductor
ax.plot(x0, y0, "ro", markersize=10, label="Conductor")
ax.legend()

st.pyplot(fig)
