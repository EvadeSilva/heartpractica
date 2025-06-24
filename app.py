import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar modelo y escalador
model = joblib.load("heart_model.pkl")
scaler = joblib.load("escalador.pkl")

st.set_page_config(page_title="Predicción de Enfermedad Cardíaca", layout="centered", page_icon="❤️")

st.title("❤️ Predicción de Enfermedad Cardíaca")
st.markdown("Esta aplicación predice si existe **riesgo de enfermedad cardíaca** basado en exámenes médicos. Los datos ingresados deben ser proporcionados por un profesional de salud.")

st.header("🔍 Ingresa los datos del paciente:")

# Diccionarios para explicaciones
sex_dict = {"Mujer": 0, "Hombre": 1}
cp_dict = {
    "Dolor típico anginoso": 0,
    "Dolor atípico anginoso": 1,
    "Dolor no anginoso": 2,
    "Asintomático": 3
}
restecg_dict = {
    "Normal": 0,
    "Anormalidad ST-T": 1,
    "Hipertrofia ventricular probable": 2
}
slope_dict = {
    "Pendiente ascendente": 0,
    "Pendiente plana": 1,
    "Pendiente descendente": 2
}
thal_dict = {
    "Normal": 1,
    "Defecto fijo": 2,
    "Defecto reversible": 3
}

# Entradas del usuario
age = st.slider("Edad", 29, 77, 50)
sex = st.selectbox("Sexo", list(sex_dict.keys()))
cp = st.selectbox("Tipo de dolor en el pecho", list(cp_dict.keys()), help="Ej: Dolor típico anginoso aparece con el esfuerzo físico y se alivia con el reposo.")
trestbps = st.slider("Presión arterial en reposo (mm Hg)", 90, 200, 120)
chol = st.slider("Colesterol sérico (mg/dl)", 100, 600, 240)
fbs = st.radio("¿Glucosa en ayunas > 120 mg/dl?", ["No", "Sí"])
restecg = st.selectbox("Resultados del electrocardiograma en reposo", list(restecg_dict.keys()))
thalach = st.slider("Frecuencia cardíaca máxima alcanzada", 70, 210, 150)
exang = st.radio("¿Angina inducida por ejercicio?", ["No", "Sí"])
oldpeak = st.slider("Depresión del segmento ST inducida por ejercicio", 0.0, 6.5, 1.0, step=0.1,
                    help="La depresión ST puede indicar isquemia inducida por ejercicio.")
slope = st.selectbox("Pendiente del segmento ST", list(slope_dict.keys()))
ca = st.slider("Número de vasos coloreados (fluoroscopía)", 0, 4, 0)
thal = st.selectbox("Resultado del test de talasemia", list(thal_dict.keys()), help="La talasemia afecta la sangre y puede influir en la salud cardíaca.")

# Convertir inputs a valores numéricos
input_data = pd.DataFrame([[
    age,
    sex_dict[sex],
    cp_dict[cp],
    trestbps,
    chol,
    1 if fbs == "Sí" else 0,
    restecg_dict[restecg],
    thalach,
    1 if exang == "Sí" else 0,
    oldpeak,
    slope_dict[slope],
    ca,
    thal_dict[thal]
]], columns=[
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope",
    "ca", "thal"
])

# Escalar datos
scaled_input = scaler.transform(input_data)

# Botón para predecir
if st.button("🔎 Predecir"):
    prediction = model.predict(scaled_input)[0]
    proba = model.predict_proba(scaled_input)[0][1]  # Probabilidad de clase positiva

    if prediction == 1:
        st.error(f"❌ El modelo predice que **Sí hay riesgo de enfermedad cardíaca** con una probabilidad del **{proba*100:.2f}%**.")
    else:
        st.success(f"✅ El modelo predice que **No hay riesgo significativo de enfermedad cardíaca** con una probabilidad del **{(1-proba)*100:.2f}%**.")

    # Interpretación adicional
    st.markdown("### 📌 Recomendaciones generales:")
    st.markdown("""
    - Consulta con un **cardiólogo** para confirmar los hallazgos.
    - Realiza pruebas adicionales como un **ecocardiograma**, **prueba de esfuerzo** o **angiografía**, según evaluación clínica.
    - Mejora hábitos alimenticios, evita el tabaquismo y realiza actividad física supervisada.
    - Mantén controlado el colesterol, la glucosa y la presión arterial.
    """)

    # Información adicional
    st.markdown("---")
    st.markdown("### ℹ️ Glosario de términos usados:")
    st.markdown("""
    - **ST**: segmento ST en un electrocardiograma, puede indicar daño o estrés cardíaco.
    - **ca**: número de vasos con anomalías detectadas por fluoroscopía.
    - **thal**: resultado de la prueba de talasemia, donde "defecto fijo" o "reversible" pueden indicar daño cardíaco previo.
    - **cp**: tipo de dolor en el pecho. Un dolor típico anginoso es el más relacionado con enfermedad coronaria.
    """)
