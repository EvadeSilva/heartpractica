import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar modelo y escalador
model = joblib.load("heart_model.pkl")
scaler = joblib.load("escalador.pkl")  # Usa el nombre correcto del archivo

st.set_page_config(page_title="Predicción de Enfermedad Cardíaca", layout="centered")

st.title("❤️ Predicción de Enfermedad Cardíaca")
st.markdown("""
Esta aplicación te ayuda a evaluar el riesgo de enfermedad cardíaca con base en tus datos clínicos.  
Por favor, llena el siguiente formulario. Si no entiendes algún término, coloca el cursor sobre el ícono (❓).
""")

# 🩺 Datos del paciente
st.sidebar.header("📝 Datos del paciente")

age = st.sidebar.slider("Edad", 29, 77, 50, help="Edad del paciente en años.")
sex = st.sidebar.selectbox("Sexo", [0, 1], format_func=lambda x: "Femenino" if x == 0 else "Masculino", help="0 = Femenino, 1 = Masculino")

cp = st.sidebar.selectbox(
    "Tipo de dolor en el pecho",
    [0, 1, 2, 3],
    format_func=lambda x: {
        0: "Angina típica (dolor al esfuerzo)",
        1: "Angina atípica (dolor menos característico)",
        2: "Dolor no anginoso (no relacionado con el corazón)",
        3: "Asintomático (sin dolor de pecho)"
    }[x],
    help="Describe la naturaleza del dolor en el pecho del paciente."
)

trestbps = st.sidebar.number_input("Presión arterial en reposo (mm Hg)", 80, 200, 120, help="Valor típico: 120 mm Hg")

chol = st.sidebar.number_input("Colesterol sérico (mg/dl)", 100, 600, 200, help="Valor normal: menor a 200 mg/dl")

fbs = st.sidebar.selectbox("¿Glucosa en ayunas > 120 mg/dl?", [0, 1], format_func=lambda x: "No" if x == 0 else "Sí", help="1 = verdadero, 0 = falso")

restecg = st.sidebar.selectbox("Resultados del electrocardiograma en reposo", [0, 1, 2],
    format_func=lambda x: {
        0: "Normal",
        1: "Anormalidad en la onda ST-T",
        2: "Hipertrofia ventricular izquierda"
    }[x],
    help="Análisis básico del ECG en reposo."
)

thalach = st.sidebar.number_input("Frecuencia cardíaca máxima alcanzada", 60, 220, 150, help="Valor típico saludable: >150")

exang = st.sidebar.selectbox("¿Angina inducida por ejercicio?", [0, 1], format_func=lambda x: "No" if x == 0 else "Sí", help="Dolor durante esfuerzo físico")

oldpeak = st.sidebar.slider("Depresión del ST", 0.0, 6.5, 1.0, 0.1, help="Medida de descenso del segmento ST tras el ejercicio (en mm). Valores altos pueden indicar isquemia.")

slope = st.sidebar.selectbox("Pendiente del ST durante el esfuerzo", [0, 1, 2],
    format_func=lambda x: {
        0: "Descendente (riesgo alto)",
        1: "Plano",
        2: "Ascendente (riesgo bajo)"
    }[x],
    help="Describe la forma de la curva ST tras el esfuerzo."
)

ca = st.sidebar.selectbox("Número de vasos principales con fluoroscopia", [0, 1, 2, 3, 4], help="Detectados mediante coloración con tinte. Mayor número puede indicar más riesgo.")

thal = st.sidebar.selectbox("Resultado de prueba 'thal'", [0, 1, 2, 3],
    format_func=lambda x: {
        0: "Desconocido",
        1: "Fijo (defecto irreversible)",
        2: "Normal",
        3: "Reversible (defecto que cambia con el esfuerzo)"
    }[x],
    help="Evaluación de flujo sanguíneo al miocardio."
)

# Procesar entrada
datos_usuario = np.array([[age, sex, cp, trestbps, chol, fbs, restecg,
                           thalach, exang, oldpeak, slope, ca, thal]])
datos_escalados = scaler.transform(datos_usuario)
prediccion = model.predict(datos_escalados)[0]
proba = model.predict_proba(datos_escalados)[0][int(prediccion)]

# Mostrar resultados
st.subheader("📊 Resultado del análisis")

if prediccion == 1:
    st.error("🔴 Posible riesgo de enfermedad cardíaca detectado.")
    st.markdown(f"**Probabilidad estimada:** {proba*100:.2f}%")
    st.info("""
Se recomienda realizar un examen clínico completo.  
Estos podrían incluir: **electrocardiograma**, **ecocardiografía**, **prueba de esfuerzo**, y análisis de sangre.
""")
else:
    st.success("🟢 No se detectan signos relevantes de enfermedad cardíaca.")
    st.markdown(f"**Probabilidad estimada de enfermedad:** {proba*100:.2f}%")
    st.info("""
No obstante, se recomienda mantener hábitos saludables y realizar chequeos regulares si existen factores de riesgo como hipertensión, obesidad o tabaquismo.
""")
