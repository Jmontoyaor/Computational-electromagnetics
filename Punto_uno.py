# C:\Users\Pc\AppData\Local\Programs\Python\Python313\python.exe -m streamlit run Punto_uno.py

# pages/2_TOBERA.py
# -*- coding: utf-8 -*-

import streamlit as st
import math
from typing import Dict, Any

# --- CUSTOM CSS STYLES ---
custom_css = """
<style>
    .stApp {
        background-color: #0e1a40;
        color: #E0E0E0;
        font-family: 'Courier New', monospace;
    }
    h1, h2, h3 {
        color: #00BFFF;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #1B1D2B;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] {
        background-color: #222f5b;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] * {
        color: #c6e2ff !important;
    }
    .resultado-final {
        color: #FFD700;
        background-color: #2c3e50;
        border: 1px solid #FFD700;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        font-size: 1.1rem;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        margin-bottom: 10px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==============================================================================
# 1. MAIN CALCULATION FUNCTION
# ==============================================================================


@st.cache_data
def analizar_tobera(
    P1_in: float, T1_in: float, V1_in: float, A1_in: float,
    P2_in: float, V2_in: float,
    unit_system: str
) -> Dict[str, Any]:
    """
    Performs thermodynamic analysis of an air nozzle, handling SI and English units.
    """
    # --- Constants for Air (in SI units) ---
    R_air_si = 0.287  # kJ/kg·K
    cp_air_si = 1.005  # kJ/kg·K

    # --- Conversion Factors ---
    KPA_TO_PSI = 0.145038
    C_TO_F_FACTOR = 9/5
    C_TO_F_OFFSET = 32
    K_TO_R = 1.8
    MS_TO_FTS = 3.28084
    CM2_TO_IN2 = 0.155
    KGS_TO_LBMS = 2.20462
    M2_TO_FT2 = 10.7639

    # --- Unit Definitions and Input Conversion ---
    units = {}
    if unit_system == 'Sistema Internacional (SI)':
        units = {
            "pressure": "kPa", "temperature_c": "°C", "temperature_k": "K",
            "velocity": "m/s", "area": "cm²", "mass_flow": "kg/s"
        }
        P1_kpa, T1_c, V1_ms, A1_cm2 = P1_in, T1_in, V1_in, A1_in
        P2_kpa, V2_ms = P2_in, V2_in
    else:  # English (Imperial) System
        units = {
            "pressure": "psi", "temperature_c": "°F", "temperature_k": "°R",
            "velocity": "ft/s", "area": "in²", "mass_flow": "lbm/s"
        }
        P1_kpa = P1_in / KPA_TO_PSI
        T1_c = (T1_in - C_TO_F_OFFSET) / C_TO_F_FACTOR
        V1_ms = V1_in / MS_TO_FTS
        A1_cm2 = A1_in / CM2_TO_IN2
        P2_kpa = P2_in / KPA_TO_PSI
        V2_ms = V2_in / MS_TO_FTS

    # --- Internal Calculations (always in SI) ---
    P1_Pa = P1_kpa * 1000
    P2_Pa = P2_kpa * 1000
    T1_K = T1_c + 273.15
    A1_m2 = A1_cm2 / 1e4

    # Mass flow rate
    v1_m3kg = (R_air_si * 1000 * T1_K) / P1_Pa
    m_dot_kgs = (A1_m2 * V1_ms) / v1_m3kg if v1_m3kg > 0 else 0

    # Outlet temperature
    Cp_J_kgK = cp_air_si * 1000
    # From h1 + V1^2/2 = h2 + V2^2/2  => Cp(T1 - T2) = (V2^2 - V1^2)/2
    delta_T_K = (V1_ms**2 - V2_ms**2) / (2 * Cp_J_kgK)
    T2_K = T1_K + delta_T_K

    # Outlet area
    v2_m3kg = (R_air_si * 1000 * T2_K) / P2_Pa if P2_Pa > 0 else 0
    A2_m2 = (m_dot_kgs * v2_m3kg) / V2_ms if V2_ms > 0 else 0

    ratio = A2_m2 / A1_m2 if A1_m2 > 0 else 0

    # --- Conversion of Results to Selected Units ---
    if unit_system == 'Sistema Inglés (Imperial)':
        m_dot_final = m_dot_kgs * KGS_TO_LBMS
        T2_final_c = (T2_K - 273.15) * C_TO_F_FACTOR + C_TO_F_OFFSET
        T2_final_k = T2_K * K_TO_R
        A2_final_cm2 = A2_m2 * M2_TO_FT2 * 144  # m2 to in2
    else:
        m_dot_final = m_dot_kgs
        T2_final_c = T2_K - 273.15
        T2_final_k = T2_K
        A2_final_cm2 = A2_m2 * 1e4

    return {
        "m_dot": m_dot_final,
        "T2_C": T2_final_c,
        "T2_K": T2_final_k,
        "A2": A2_final_cm2,
        "ratio": ratio,
        "units": units
    }


# --- PAGE LAYOUT ---
col_img, col_title = st.columns([0.2, 1])
with col_img:
    st.image("https://raw.githubusercontent.com/Jmontoyaor/thermodynamics/main/IMAGENES/Toberas.png", width=200)
with col_title:
    st.title("Tobera: Análisis Interactivo de Tobera de Aire")
st.markdown(
    "#### Explora cómo varían la velocidad, la presión y la temperatura en una tobera.")
st.write("---")

# --- THEORY SECTION ---
with st.expander("📘 Fundamentos Termodinámicos de Toberas y Difusores (Çengel, 7ª ed.)"):
    st.markdown(r"""
    Las **toberas** y los **difusores** son dispositivos fundamentales en sistemas de propulsión como motores a chorro, cohetes, turbinas de gas y también en aplicaciones industriales.
    - Una **tobera** incrementa la **velocidad del fluido** a costa de una **disminución de la presión**.
    - Un **difusor**, en cambio, **disminuye la velocidad** del fluido mientras **aumenta su presión**.

    Ambos dispositivos están diseñados para modificar la energía cinética del fluido que los atraviesa, y **no implican trabajo mecánico** ($\dot{W} \equiv 0$), ni transferencia de calor significativa ($\dot{Q} \approx 0$), y el cambio de energía potencial es despreciable ($\Delta ep \approx 0$).

    Por ello, la **conservación de energía** (1ª Ley de la Termodinámica para sistemas abiertos) se simplifica en estos casos a:

    $$
    h_1 + \frac{V_1^2}{2} = h_2 + \frac{V_2^2}{2}
    $$

    donde:
    - $h = C_p T$ es la entalpía específica para un gas ideal.
    - $V$ es la velocidad del flujo

    Esto permite determinar la **temperatura de salida** $T_2$ si se conocen $T_1$, $V_1$ y $V_2$.

    Asimismo, al aplicar la ecuación de conservación de masa:

    $$
    \dot{m} = \frac{A_1 V_1}{v_1} = \frac{A_2 V_2}{v_2}
    $$

    es posible calcular el **área de salida** $A_2$, siendo:
    - $v = \dfrac{RT}{P}$ el volumen específico del aire como gas ideal.

    📚 **Fuente**: Çengel, Yunus A., *Termodinámica*, 7ª Edición, McGraw-Hill, Sección 5.4 "Toberas y Difusores", pp. 278–279.
    """)

# --- EXERCISE SECTION ---
col1, col2 = st.columns(2)
with col1:
    with st.expander("🧪 Ejercicio Propuesto – Toberas"):
        st.markdown("""
        **Primera ley de la termodinámica – Sistemas Abiertos**

        **TOBERAS**

        La entrada de una tobera tiene una sección de 100 cm², y por ella entra aire a una velocidad de 50 m/s, con una presión de 350 kPa y una temperatura de 227 °C. Luego sale a una velocidad de 190 m/s y una presión de 120 kPa. Determinar:

        - a) El flujo másico de aire que circula por la tobera
        - b) La temperatura del aire a la salida de la tobera
        - c) El área de sección de salida de la tobera
        - d) La relación de áreas de entrada y salida

        ---

        **Fuente:** *Ejercicio tomado y adaptado de **LaMejorAsesoríaEducativa – YouTube***.
        """)
with col2:
    st.image("https://raw.githubusercontent.com/Jmontoyaor/thermodynamics/main/IMAGENES/Imagen%201.png",
             caption="**FIGURA 5-25** – La forma de toberas y difusores es tal que causan grandes cambios en la velocidad del fluido y, por lo tanto, en la energía cinética.\n\nFuente: Çengel – Termodinámica, 7ª Edición.")
    st.markdown("### Desarrollo visual")
    # Placeholder video
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
st.markdown("---")

# --- SIDEBAR WITH INPUT CONTROLS ---
st.sidebar.header("📥 Parámetros de Entrada")
unit_system = st.sidebar.radio("Seleccione el Sistema de Unidades",
                               ('Sistema Internacional (SI)', 'Sistema Inglés (Imperial)'))

if unit_system == 'Sistema Internacional (SI)':
    P1 = st.sidebar.slider(
        "Presión entrada P₁ [kPa]", 50.0, 1000.0, 350.0, 10.0)
    T1 = st.sidebar.slider(
        "Temperatura entrada T₁ [°C]", -50.0, 800.0, 227.0, 5.0)
    V1 = st.sidebar.slider("Velocidad entrada V₁ [m/s]", 1.0, 500.0, 50.0, 1.0)
    A1 = st.sidebar.slider("Área entrada A₁ [cm²]", 1.0, 1000.0, 100.0, 1.0)
    P2 = st.sidebar.slider("Presión salida P₂ [kPa]", 5.0, 1000.0, 120.0, 5.0)
    V2 = st.sidebar.slider(
        "Velocidad salida V₂ [m/s]", 1.0, 1000.0, 190.0, 1.0)
else:  # English System
    P1 = st.sidebar.slider("Presión entrada P₁ [psi]", 7.0, 150.0, 50.8, 1.0)
    T1 = st.sidebar.slider(
        "Temperatura entrada T₁ [°F]", -58.0, 1500.0, 440.0, 10.0)
    V1 = st.sidebar.slider(
        "Velocidad entrada V₁ [ft/s]", 3.0, 1600.0, 164.0, 5.0)
    A1 = st.sidebar.slider("Área entrada A₁ [in²]", 0.1, 160.0, 15.5, 0.5)
    P2 = st.sidebar.slider("Presión salida P₂ [psi]", 0.7, 150.0, 17.4, 0.5)
    V2 = st.sidebar.slider(
        "Velocidad salida V₂ [ft/s]", 3.0, 3300.0, 623.0, 10.0)

# --- EXECUTION AND RESULT PRESENTATION ---
resultados = analizar_tobera(P1, T1, V1, A1, P2, V2, unit_system)
units = resultados['units']

st.header("📊 Resultados del Análisis")
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f"<div class='resultado-final'><strong>Flujo másico (ṁ):</strong><br>{resultados['m_dot']:.3f} {units['mass_flow']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='resultado-final'><strong>Área de salida (A₂):</strong><br>{resultados['A2']:.2f} {units['area']}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(
        f"<div class='resultado-final'><strong>Temperatura de salida (T₂):</strong><br>{resultados['T2_C']:.2f} {units['temperature_c']} ({resultados['T2_K']:.2f} {units['temperature_k']})</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='resultado-final'><strong>Relación de áreas (A₂/A₁):</strong><br>{resultados['ratio']:.4f}</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Developed by Juan Fernando Montoya Ortiz - Electrical Engineering Student - Universidad Nacional de Colombia")
