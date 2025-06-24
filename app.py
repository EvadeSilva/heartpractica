import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar modelo y escalador
model = joblib.load("heart_model.pkl")
scaler = joblib.load("escalador.pkl")

st.set_page_config(page_title="Predicción de Enfermedad Cardíaca", layout="centered")

st.title("💖 Predicción de Enfermedad Cardíaca")
st.markdown(
    """
    Esta aplicación predice la probabilidad de que una persona presente una enfermedad cardíaca, 
    basándose en indicadores clínicos comunes. Llena el formulario con los datos del paciente. 
    Los valores normales y explicaciones están disponibles en cada campo.
    """
)

st.sidebar.header("📋 Formulario de Datos del Paciente")

# === Formulario ===
age = st.sidebar.slider("Edad", 29, 77, 50, help="Edad del paciente. A mayor edad, mayor riesgo.")
sex = st.sidebar.selectbox("Sexo biológico", ["Femenino", "Masculino"], help="El sexo masculino tiene un riesgo cardiovascular ligeramente mayor.")

cp = st.sidebar.selectbox(
    "Tipo de dolor en el pecho",
    ["0 = Angina típica", "1 = Angina atípica", "2 = Dolor no anginoso", "3 = Asintomático"],
    help="Tipo 0: Dolor relacionado con esfuerzo. Tipo 3: No hay síntomas, pero puede haber enfermedad oculta."
)

trestbps = st.sidebar.number_input(
    "Presión arterial en reposo (mm Hg)",
    min_value=80, max_value=200, value=120,
    help="Presión normal: <120 mm Hg. Mayor a eso puede indicar hipertensión."
)

chol = st.sidebar.number_input(
    "Colesterol sérico (mg/dL)",
    min_value=100, max_value=600, value=200,
    help="Valor normal: <200 mg/dL. Valores elevados son un factor de riesgo importante."
)

fbs = st.sidebar.selectbox(
    "¿Glucemia en ayunas > 120 mg/dL?",
    ["No", "Sí"],
    help="La glucosa elevada en ayunas puede indicar diabetes o prediabetes."
)

restecg = st.sidebar.selectbox(
    "Electrocardiograma en reposo",
    ["0 = Normal", "1 = Anomalía onda ST-T", "2 = Hipertrofia ventricular izquierda"],
    help="El ECG puede mostrar señales de problemas cardíacos incluso sin síntomas."
)

thalach = st.sidebar.slider(
    "Frecuencia cardíaca máxima alcanzada",
    min_value=70, max_value=210, value=150,
    help="Normal según edad: 220 - edad. Un valor bajo podría indicar un corazón débil."
)

exang = st.sidebar.selectbox(
    "¿Dolor en el pecho inducido por ejercicio (angina)?",
    ["No", "Sí"],
    help="Indica si el esfuerzo físico causa dolor en el pecho (síntoma común de enfermedad coronaria)."
)

oldpeak = st.sidebar.slider(
    "Depresión del ST tras el ejercicio",
    min_value=0.0, max_value=6.5, value=1.0,
    help="Mide cambios en el electrocardiograma tras el ejercicio. Valores >1.0 pueden indicar isquemia (falta de oxígeno en el corazón)."
)

slope = st.sidebar.selectbox(
    "Pendiente del segmento ST",
    ["0 = Descendente", "1 = Plana", "2 = Ascendente"],
    help="El segmento ST en ECG puede reflejar problemas. Una pendiente descendente suele ser preocupante."
)

ca = st.sidebar.selectbox(
    "Número de vasos coloreados por fluoroscopía (0-4)",
    ["0", "1", "2", "3", "4"],
    help="Más vasos coloreados indica mayor posibilidad de obstrucción coronaria visible."
)

thal = st.sidebar.selectbox(
    "Resultado del estudio de talio (thalassemia)",
    ["1 = Defecto fijo", "2 = Normal", "3 = Defecto reversible"],
    help="El defecto reversible sugiere posible obstrucción que mejora con el reposo, lo que puede indicar enfermedad cardíaca."
)

# ==== Botón de predicción ====
if st.sidebar.button("📈 Predecir"):
    input_dict = {
        "age": age,
        "sex": 1 if sex == "Masculino" else 0,
        "cp": int(cp[0]),
        "trestbps": trestbps,
        "chol": chol,
        "fbs": 1 if fbs == "Sí" else 0,
        "restecg": int(restecg[0]),
        "thalach": thalach,
        "exang": 1 if exang == "Sí" else 0,
        "oldpeak": oldpeak,
        "slope": int(slope[0]),
        "ca": int(ca),
        "thal": int(thal[0])
    }

    input_df = pd.DataFrame([input_dict])
    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][int(prediction)]

    st.subheader("📊 Resultado del análisis")

    if prediction == 1:
        st.error("🔴 Posible riesgo de enfermedad cardíaca detectado.")
    else:
        st.success("🟢 No se detecta riesgo significativo de enfermedad cardíaca.")

    st.markdown(f"**Probabilidad estimada:** {probability:.2%}")

    st.info(
        "Se recomienda realizar un examen clínico completo. "
        "Estos podrían incluir: **electrocardiograma**, **ecocardiografía**, "
        "**prueba de esfuerzo** o **análisis de sangre**."
    )
