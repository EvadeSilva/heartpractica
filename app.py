import streamlit as st
import pandas as pd
import joblib

# Cargar modelo y scaler
model = joblib.load("heart_model.pkl")
scaler = joblib.load("escalador.pkl")

# Diccionarios de traducción
cp_dict = {
    "Dolor típico anginoso": 0,
    "Dolor atípico anginoso": 1,
    "Dolor no anginoso": 2,
    "Asintomático": 3
}
restecg_dict = {
    "Normal": 0,
    "Anormalidad ST-T": 1,
    "Hipertrofia ventricular izquierda": 2
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

# Interfaz de la app
st.set_page_config(page_title="🫀 Predicción de Enfermedad Cardíaca", layout="centered", initial_sidebar_state="auto")

st.title("🩺 Predicción de Enfermedad Cardiaca")
st.markdown("Esta aplicación predice si una persona tiene riesgo de enfermedad cardíaca basándose en varios factores clínicos. Ingresa los datos del paciente para obtener una predicción.")

# Formulario de entrada
with st.form("input_form"):
    st.subheader("🔍 Ingresa los datos del paciente:")
    
    age = st.slider("Edad", 29, 77, 50)
    sex = st.radio("Sexo", ["Mujer", "Hombre"])
    
    cp = st.selectbox("Tipo de dolor en el pecho", list(cp_dict.keys()))
    trestbps = st.slider("Presión arterial en reposo (mm Hg)", 80, 200, 120)
    chol = st.slider("Colesterol sérico (mg/dl)", 100, 600, 240)
    
    fbs = st.radio("¿Glucosa en ayunas mayor a 120 mg/dl?", ["Sí", "No"])
    
    restecg = st.selectbox("Resultado del ECG en reposo", list(restecg_dict.keys()))
    thalach = st.slider("Frecuencia cardíaca máxima alcanzada", 70, 210, 150)
    
    exang = st.radio("¿Angina inducida por ejercicio?", ["Sí", "No"])
    oldpeak = st.slider("Depresión ST inducida por ejercicio", 0.0, 6.5, 1.0, step=0.1)
    
    slope = st.selectbox("Pendiente del segmento ST", list(slope_dict.keys()))
    ca = st.slider("Número de vasos coloreados (fluoroscopía)", 0, 4, 0)
    
    thal = st.selectbox("Resultado del test de talasemia", list(thal_dict.keys()))
    
    submitted = st.form_submit_button("Predecir")

# Al hacer clic en el botón
if submitted:
    input_data = pd.DataFrame([[
        age,
        1 if sex == "Hombre" else 0,
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
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope',
        'ca', 'thal'
    ])
    
    # Escalar
    input_scaled = scaler.transform(input_data)
    
    # Predicción
    prediction = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0][int(prediction)]

    # Mostrar resultado
    if prediction == 1:
        st.error(f"❌ El modelo predice que **sí hay riesgo de enfermedad cardíaca** con una probabilidad de {prob:.2%}.")
    else:
        st.success(f"✅ El modelo predice que **no hay riesgo de enfermedad cardíaca** con una probabilidad de {prob:.2%}.")

    st.markdown("---")
    st.caption("🔬 Este modelo fue entrenado con datos del conjunto `heart-disease` y optimizado con Random Forest.")
