import streamlit as st
import json
from typing import Dict, List

# --- CONFIGURACIÓN DE PÁGINA Y ESTILOS ---
st.set_page_config(
    layout="wide",
    page_title="Quiz de Electromagnetismo",
    page_icon="🤖"
)

# CSS personalizado con tu paleta de colores preferida
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #0e1a40;
        color: #E0E0E0;
        font-family: 'Poppins', sans-serif;
    }

    h1, h2, h3 {
        color: #00BFFF;
        font-family: 'Poppins', sans-serif;
    }

    section[data-testid="stSidebar"] {
        background-color: #222f5b !important;
        border-radius: 10px;
        font-family: 'Poppins', sans-serif;
    }

    section[data-testid="stSidebar"] * {
        color: #c6e2ff !important;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #222f5b, #0e1a40);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        border: 2px solid #00BFFF;
        box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.2);
    }

    .quiz-container {
        background: linear-gradient(135deg, rgba(34, 47, 91, 0.8), rgba(14, 26, 64, 0.9));
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 191, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.1);
    }

    .question-number {
        background: linear-gradient(45deg, #00BFFF, #222f5b);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(0, 191, 255, 0.3);
    }

    .stRadio > div {
        background: rgba(34, 47, 91, 0.4);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 191, 255, 0.2);
        color: #ffffff !important;
    }

    .stRadio > div > label {
        color: #ffffff !important;
    }

    .stRadio > div > label > div {
        color: #ffffff !important;
    }

    .stRadio label {
        color: #ffffff !important;
    }

    /* Asegurar que todas las opciones de radio sean blancas */
    div[data-testid="stRadio"] label span {
        color: #ffffff !important;
    }

    div[data-testid="stRadio"] > div > label {
        color: #ffffff !important;
    }

    .result-correct {
        background: linear-gradient(45deg, #00BFFF, #222f5b);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0, 191, 255, 0.3);
    }

    .result-incorrect {
        background: linear-gradient(45deg, #ff4757, #222f5b);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
    }

    .hint-box {
        background: rgba(34, 47, 91, 0.6);
        border-left: 4px solid #00BFFF;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-style: italic;
        color: #c6e2ff;
    }

    .score-container {
        text-align: center;
        background: linear-gradient(135deg, #222f5b, #00BFFF);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px 0 rgba(0, 191, 255, 0.4);
        border: 2px solid rgba(0, 191, 255, 0.5);
    }

    .stButton > button {
        background: linear-gradient(45deg, #00BFFF, #222f5b);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 191, 255, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 191, 255, 0.4);
        background: linear-gradient(45deg, #0099cc, #1a2547);
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00BFFF, #222f5b);
    }

    .stMetric {
        background: rgba(34, 47, 91, 0.6);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(0, 191, 255, 0.2);
    }

    .stExpander {
        background: rgba(34, 47, 91, 0.4);
        border: 1px solid rgba(0, 191, 255, 0.2);
        border-radius: 10px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --- DATOS DEL QUIZ ---
quiz_data = {
    "title": "⚡ Quiz de Electromagnetismo Computacional",
    "description": "Pon a prueba tus conocimientos sobre campos eléctricos, densidades de carga y fundamentos de electrostática y modelado computacional.",
    "questions": [
        {
            "id": 1,
            "question": "¿Qué nombre recibe la técnica numérica que aproxima integrales mediante áreas de trapecios?",
            "options": [
                "Regla de Simpson",
                "Regla del trapecio",
                "Método de Newton",
                "Serie de Taylor"
            ],
            "correct_answer": 1,
            "explanation": "La regla del trapecio aproxima integrales sumando áreas de trapecios formados en subintervalos iguales.",
            "hint": "Piensa en dividir el área bajo la curva en figuras simples."
        },
        {
            "id": 2,
            "question": "Si un cuerpo tiene equilibrio a lo largo de una línea cargada, ¿qué densidad de carga se usa?",
            "options": [
                "Densidad superficial de carga (σ)",
                "Densidad volumétrica de carga (ρ)",
                "Densidad lineal de carga (λ)",
                "Densidad angular de carga"
            ],
            "correct_answer": 2,
            "explanation": "Para cargas distribuidas en una línea, se usa la densidad lineal de carga λ = Q/L.",
            "hint": "Carga dividida entre longitud."
        },
        {
            "id": 3,
            "question": "¿Cuál de los siguientes es un ejemplo de campo escalar?",
            "options": [
                "La velocidad del viento en un punto",
                "La temperatura en una ciudad",
                "La fuerza sobre una partícula",
                "El campo eléctrico en un punto"
            ],
            "correct_answer": 1,
            "explanation": "La temperatura asigna un valor único (escalar) en cada punto del espacio.",
            "hint": "No tiene dirección, solo magnitud."
        },
        {
            "id": 4,
            "question": "El modelo microscópico en electromagnetismo computacional se basa en:",
            "options": [
                "Ignorar cargas y modelar solo campos.",
                "Considerar cargas individuales e interacciones mediante leyes como Coulomb, Gauss, Faraday y Ampère.",
                "Explicar sin electrones ni protones.",
                "Usar solo aproximaciones macroscópicas."
            ],
            "correct_answer": 1,
            "explanation": "El modelo microscópico describe el campo desde partículas y leyes fundamentales.",
            "hint": "Parte desde cargas elementales y sus interacciones."
        },
        {
            "id": 5,
            "question": "¿Cómo se denomina la magnitud de carga eléctrica por unidad de volumen?",
            "options": [
                "Densidad lineal de carga (λ)",
                "Densidad superficial de carga (σ)",
                "Densidad volumétrica de carga (ρ)",
                "Intensidad de campo eléctrico"
            ],
            "correct_answer": 2,
            "explanation": "La densidad volumétrica es ρ = Q/V, en [C/m³].",
            "hint": "Se mide respecto al espacio tridimensional."
        },
        {
            "id": 6,
            "question": "¿Qué se entiende por electricidad estática o electrostática?",
            "options": [
                "Estudio de cargas en movimiento",
                "Estudio de campos magnéticos en reposo",
                "Estudio de cargas en reposo y sus interacciones",
                "Estudio de ondas electromagnéticas"
            ],
            "correct_answer": 2,
            "explanation": "La electrostática estudia cargas en reposo y los campos que generan.",
            "hint": "No hay movimiento de cargas."
        },
        {
            "id": 7,
            "question": "Relaciona cada densidad de carga con su fórmula correcta:",
            "options": [
                "λ = Q/L  [C/m]",
                "σ = Q/S  [C/m²]",
                "ρ = Q/V  [C/m³]",
                "Todas las anteriores"
            ],
            "correct_answer": 3,
            "explanation": "Las tres son correctas: lineal (λ), superficial (σ) y volumétrica (ρ).",
            "hint": "Cada tipo depende de la dimensión de la región cargada."
        }
    ]
}


# --- INICIALIZACIÓN DEL ESTADO ---
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

# --- FUNCIONES AUXILIARES ---


def reset_quiz():
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.show_results = False
    st.session_state.quiz_completed = False


def calculate_score():
    correct = 0
    total = len(quiz_data['questions'])
    for q_id, answer in st.session_state.answers.items():
        question = next(q for q in quiz_data['questions'] if q['id'] == q_id)
        if answer == question['correct_answer']:
            correct += 1
    return correct, total


# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🧑‍💻 Quiz de Electromagnetismo</h1>
    <h3>🧠 Electromagnetismo computacional</h3>
    <p>Pon a prueba tus conocimientos sobre campos eléctricos, densidades de carga y fundamentos de electrostática y modelado computacional</p>
</div>
""", unsafe_allow_html=True)

# --- LÓGICA PRINCIPAL DEL QUIZ ---
if not st.session_state.quiz_completed:
    current_q_index = st.session_state.current_question

    if current_q_index < len(quiz_data['questions']):
        question = quiz_data['questions'][current_q_index]

        st.markdown(f"""
        <div class="quiz-container">
            <div class="question-number">Pregunta {current_q_index + 1} de {len(quiz_data['questions'])}</div>
        </div>
        """, unsafe_allow_html=True)

        # Barra de progreso
        progress = (current_q_index + 1) / len(quiz_data['questions'])
        st.progress(progress)

        # Pregunta
        st.markdown(f"""
        <div class="quiz-container">
            <h3>💡 {question['question']}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Opciones de respuesta
        with st.container():
            answer = st.radio(
                "Selecciona tu respuesta:",
                options=range(len(question['options'])),
                format_func=lambda x: question['options'][x],
                key=f"q_{question['id']}"
            )

        # Mostrar pista
        with st.expander("💡 Ver pista"):
            st.markdown(f"""
            <div class="hint-box">
                <strong>Pista:</strong> {question['hint']}
            </div>
            """, unsafe_allow_html=True)

        # Botones de navegación
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if current_q_index > 0:
                if st.button("⬅️ Anterior", key="prev_btn"):
                    st.session_state.current_question -= 1
                    st.rerun()

        with col3:
            if st.button("Siguiente ➡️", key="next_btn"):
                # Guardar respuesta
                st.session_state.answers[question['id']] = answer

                if current_q_index == len(quiz_data['questions']) - 1:
                    # Última pregunta - completar quiz
                    st.session_state.quiz_completed = True
                    st.rerun()
                else:
                    # Siguiente pregunta
                    st.session_state.current_question += 1
                    st.rerun()

# --- MOSTRAR RESULTADOS ---
if st.session_state.quiz_completed:
    correct, total = calculate_score()
    percentage = (correct / total) * 100

    # Resultado general
    st.markdown(f"""
    <div class="score-container">
        <h2>🎉 ¡Quiz Completado! 🎉</h2>
        <h1>{correct}/{total}</h1>
        <h3>Puntuación: {percentage:.1f}%</h3>
        <p>{"¡Excelente trabajo! 🌟" if percentage >= 80 else "¡Buen intento! 👍" if percentage >= 60 else "¡Sigue practicando! 📚"}</p>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar respuestas detalladas
    st.markdown("## 📋 Revisión de Respuestas")

    for question in quiz_data['questions']:
        q_id = question['id']
        user_answer = st.session_state.answers.get(q_id, -1)
        is_correct = user_answer == question['correct_answer']

        # Contenedor de pregunta
        st.markdown(f"""
        <div class="quiz-container">
            <h4>Pregunta {q_id}: {question['question']}</h4>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar resultado
        if is_correct:
            st.markdown(f"""
            <div class="result-correct">
                ✅ <strong>Correcto!</strong><br>
                Tu respuesta: {question['options'][user_answer]}<br>
                <strong>Explicación:</strong> {question['explanation']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-incorrect">
                ❌ <strong>Incorrecto</strong><br>
                Tu respuesta: {question['options'][user_answer] if user_answer >= 0 else "Sin respuesta"}<br>
                Respuesta correcta: {question['options'][question['correct_answer']]}<br>
                <strong>Explicación:</strong> {question['explanation']}
            </div>
            """, unsafe_allow_html=True)

    # Botón para reiniciar
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Reiniciar Quiz", key="restart_btn"):
            reset_quiz()
            st.rerun()

# --- SIDEBAR CON INFO ---
with st.sidebar:
    st.markdown("""
    ### 📊 Estadísticas del Quiz
    """)

    if st.session_state.quiz_completed:
        correct, total = calculate_score()
        st.metric("Preguntas Respondidas", f"{total}/{total}")
        st.metric("Respuestas Correctas", correct)
        st.metric("Puntuación", f"{(correct/total)*100:.1f}%")
    else:
        answered = len(st.session_state.answers)
        st.metric(
            "Progreso", f"{st.session_state.current_question + 1}/{len(quiz_data['questions'])}")
        st.metric("Respuestas Guardadas", answered)

    st.markdown("""
    ---
    ### 💡 Consejos
    - Lee cada pregunta cuidadosamente
    - Usa las pistas si necesitas ayuda
    - Puedes regresar a preguntas anteriores
    - Al final verás explicaciones detalladas
    """)

    st.markdown("""
    ---
    ### 🎯 Temas Cubiertos
    - Métodos numéricos básicos en electromagnetismo 
    - Diferencia entre campos escalares y vectoriales
    - Modelos microscópicos vs. macroscópicos en electromagnetismo
    - Conceptos fundamentales de electrostática (cargas en reposo e interacciones)
    - Fundamentos del modelado computacional de campos eléctricos
    """)
