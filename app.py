import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar modelo y escalador
model = joblib.load("heart_model.pkl")
scaler = joblib.load("escalador.pkl")

st.set_page_config(page_title="Predicción de Enfermedad Cardíaca", layout="centered")
st.title("🫀 Predicción de Enfermedad Cardíaca")
st.markdown("Esta aplicación predice la probabilidad de que una persona presente una enfermedad cardíaca, basándose en indicadores clínicos comunes. Llena el formulario con los datos del paciente. Los valores normales y explicaciones están disponibles en cada campo.")

st.sidebar.header("🔍 Ingresa los datos del paciente")

age = st.sidebar.slider("Edad", 29, 77, 50, help="La edad es un factor de riesgo importante. Mayores de 45 años tienen más riesgo.")

sex = st.sidebar.selectbox("Sexo biológico", ["Femenino", "Masculino"], help="El sexo masculino tiene mayor riesgo estadístico.")

cp = st.sidebar.selectbox(
    "Tipo de dolor en el pecho",
    ["0 = Angina típica", "1 = Angina atípica", "2 = Dolor no anginoso", "3 = Asintomático"],
    help=(
        "Tipo 0: Dolor típico relacionado con el esfuerzo.\n"
        "Tipo 1: Dolor atípico, no necesariamente relacionado al corazón.\n"
        "Tipo 2: Dolor no cardíaco.\n"
        "Tipo 3: Sin síntomas, aunque pueda haber enfermedad."
    )
)

trestbps = st.sidebar.number_input(
    "Presión arterial en reposo (mm Hg)",
    80, 200, 120,
    help="Presión normal: <120 mm Hg. Valores mayores pueden indicar hipertensión."
)

chol = st.sidebar.number_input(
    "Colesterol sérico (mg/dL)",
    100, 600, 200,
    help="Colesterol normal: <200 mg/dL. Niveles elevados aumentan el riesgo cardíaco."
)

fbs = st.sidebar.selectbox(
    "¿Glucemia en ayunas > 120 mg/dL?",
    ["No", "Sí"],
    help="Glucosa en ayunas elevada puede indicar diabetes o prediabetes."
)

restecg = st.sidebar.selectbox(
    "Resultados del electrocardiograma en reposo",
    ["0 = Normal", "1 = Anormalidad leve (ST-T)", "2 = Hipertrofia ventricular"],
    help="0: Normal\n1: Alteraciones leves de la onda ST o T\n2: Engrosamiento del músculo cardíaco."
)

thalach = st.sidebar.number_input(
    "Frecuencia cardíaca máxima alcanzada",
    60, 220, 150,
    help="Varía con la edad. Ej: para 50 años, normal ≈ 170 lpm (220 - edad)."
)

exang = st.sidebar.selectbox(
    "¿Dolor por ejercicio (angina inducida)?",
    ["No", "Sí"],
    help="¿El dolor en el pecho aparece con el esfuerzo físico?"
)

oldpeak = st.sidebar.number_input(
    "Depresión del ST inducida por ejercicio",
    0.0, 6.5, 1.0,
    help="Representa cambios en el ECG tras el ejercicio. Valores >1.0 pueden indicar isquemia."
)

slope = st.sidebar.selectbox(
    "Pendiente del segmento ST durante ejercicio",
    ["0 = Descendente", "1 = Plana", "2 = Ascendente"],
    help="Indica la forma de la curva ST en el ECG.\n0: Descendente (riesgo alto)\n2: Ascendente (normal)."
)

ca = st.sidebar.selectbox(
    "Número de vasos principales coloreados por fluoroscopía",
    ["0", "1", "2", "3", "4"],
    help="0 es normal. Más vasos coloreados puede indicar obstrucciones coronarias visibles."
)

thal = st.sidebar.selectbox(
    "Resultado del test de talio (thalassemia)",
    ["1 = Fijo", "2 = Normal", "3 = Reversible"],
    help="1: Defecto fijo (probable daño permanente).\n2: Normal\n3: Defecto reversible (posible obstrucción reversible)."
)

# Procesamiento de entradas
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

# Predicción
if st.button("📈 Predecir"):
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][int(prediction)]

    if prediction == 1:
        st.error(f"⚠️ Alta probabilidad de enfermedad cardíaca ({probability:.2%})")
    else:
        st.success(f"✅ Baja probabilidad de enfermedad cardíaca ({probability:.2%})")

    st.markdown("**Nota:** Esta predicción no reemplaza un diagnóstico médico profesional.")
