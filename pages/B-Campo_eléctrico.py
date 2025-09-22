
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
    st.image("https://raw.githubusercontent.com/Jmontoyaor/Computational-electromagnetics/main/Imagenes/Distribucci%C3%B3n.png", width=150)

with col_title:
    st.title("Campo Eléctrico")

# Texto introductorio actualizado
st.markdown("#### Descubre qué es un campo eléctrico, cómo se representa en el espacio-tiempo y cómo se calcula su intensidad.")
st.write("---")

# --- CUERPO TEÓRICO ---
st.header("Fundamentos Teóricos del Campo Eléctrico")

# Subsección 1: Concepto
st.subheader("1. Concepto de Campo Eléctrico")
st.markdown(r"""
El **campo eléctrico** es una magnitud vectorial que describe la interacción a distancia entre cuerpos cargados. Se define como la fuerza ($\vec{F}$) que experimenta una carga de prueba positiva ($q$) al colocarse en un punto del espacio, dividida por el valor de dicha carga.
""")
st.latex(r"\vec{E} = \frac{\vec{F}}{q}")
st.markdown("""
Su naturaleza vectorial implica que en cada punto del espacio se asigna un vector que indica la dirección y el sentido de la fuerza que actuaría sobre una carga positiva.
""")

# Subsección 2: Ubicación Espacio-Temporal
st.subheader("2. Ubicación Espacio-Temporal en un Campo")
st.markdown("""
La descripción de un campo no solo depende del espacio, sino también del tiempo. Un campo puede clasificarse en:
- **Campo estático:** Solo varía en el espacio, es constante en el tiempo.
- **Campo dinámico:** Varía tanto en el espacio como en el tiempo, modelando fenómenos como las ondas electromagnéticas.

La ubicación espacio-temporal de un campo eléctrico se expresa como una función vectorial de las cuatro variables (x, y, z, t):
""")
st.latex(r"\vec{E} = \vec{E}(x,y,z,t)")

# Subsección 3: Intensidad
st.subheader("3. Intensidad de Campo Eléctrico")
st.markdown(r"""
La intensidad del campo eléctrico cuantifica la magnitud de la fuerza que una carga fuente ($Q$) ejerce en un punto del espacio. Este concepto se basa en la **Ley de Coulomb**.

La expresión para el campo eléctrico generado por una carga puntual es:
""")
st.latex(r"\vec{E} = \frac{1}{4\pi \epsilon_0} \frac{Q}{|\vec{r}|^2} \hat{r}")
st.markdown(r"""
Donde:
- **$Q$** es la carga fuente.
- **$\vec{r}$** es el vector de posición desde la carga fuente al punto de observación.
- **$\hat{r}$** es el vector unitario en la dirección de $\vec{r}$.
- **$\epsilon_0$** es la permitividad eléctrica del vacío.
""")


# --- Constante de Coulomb ---
k = 8.987e9  # N·m²/C²

# --- Función para calcular el campo eléctrico de una carga puntual ---


def campo_electrico_punto(q, r_carga, r_eval):
    r_vec = r_eval - r_carga
    r_mag = np.linalg.norm(r_vec)
    if r_mag < 1e-6:
        return np.array([0, 0])
    r_unit = r_vec / r_mag
    return k * q * r_unit / r_mag**2


# --- Interfaz en Streamlit ---
st.title("⚡ Visualización del Campo Eléctrico con 3 Cargas Puntuales")

st.header("🔧 Parámetros de las cargas")

# Tres columnas para las tres cargas
col1, col2, col3 = st.columns(3)
cargas = []

for i, col in enumerate([col1, col2, col3]):
    with col:
        st.subheader(f"Carga {i+1}")
        q = st.slider(f"q{i+1} (nC)", -5.0, 5.0, 1.0, step=0.1, key=f"q{i}")
        x = st.slider(f"x{i+1} (m)", -6.0, 6.0,
                      float(i*2 - 2), step=0.1, key=f"x{i}")
        y = st.slider(f"y{i+1} (m)", -6.0, 6.0,
                      float(i - 1), step=0.1, key=f"y{i}")
        cargas.append({'q': q*1e-9, 'pos': np.array([x, y])})


# --- Preparación de la malla ---
nx, ny = 40, 40
x = np.linspace(-6, 6, nx)
y = np.linspace(-6, 6, ny)
X, Y = np.meshgrid(x, y)

Ex, Ey = np.zeros(X.shape), np.zeros(Y.shape)

# --- Cálculo del campo ---
for i in range(nx):
    for j in range(ny):
        punto_eval = np.array([X[i, j], Y[i, j]])
        E_total = np.array([0.0, 0.0])
        for carga in cargas:
            E_total += campo_electrico_punto(carga['q'],
                                             carga['pos'], punto_eval)
        Ex[i, j] = E_total[0]
        Ey[i, j] = E_total[1]

# --- Visualización ---
fig, ax = plt.subplots(figsize=(8, 8))

magnitud = np.sqrt(Ex**2 + Ey**2)
Ex_norm = Ex / magnitud
Ey_norm = Ey / magnitud

quiver = ax.quiver(X, Y, Ex_norm, Ey_norm, magnitud, cmap='viridis', scale=40)
plt.colorbar(quiver, ax=ax, label='Magnitud del Campo Eléctrico (N/C)')

# Dibujar cargas
for carga in cargas:
    color = 'blue' if carga['q'] > 0 else 'red'
    ax.scatter(carga['pos'][0], carga['pos'][1], color=color,
               s=150, zorder=5, edgecolors='white')
    ax.text(carga['pos'][0] + 0.2, carga['pos'][1] +
            0.2, f'{carga["q"]*1e9:.1f} nC', fontsize=10)

ax.set_title('Campo Eléctrico de Cargas Puntuales')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.axis('equal')
ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.grid(True, linestyle=':', alpha=0.6)

st.pyplot(fig)
