import streamlit as st
import pandas as pd
import joblib

# Título
st.title("🫀 Predicción de Enfermedad Cardíaca")

# Cargar modelo
@st.cache(allow_output_mutation=True)
def load_model():
    return joblib.load("heart_model.pkl")

model = load_model()

# Interfaz de usuario mejorada
st.subheader("🔍 Ingresa los datos del paciente:")

age = st.slider("Edad (años)", 29, 77, 50)
sex = st.radio("Sexo", options=[0, 1], format_func=lambda x: "Mujer" if x == 0 else "Hombre")
cp = st.radio("Tipo de dolor en el pecho",
              options=[0, 1, 2, 3],
              format_func=lambda x: [
                  "0: Angina típica",
                  "1: Angina atípica",
                  "2: Dolor no anginoso",
                  "3: Asintomático"
              ][x])
trestbps = st.number_input("Presión arterial en reposo (mm Hg)", min_value=90, max_value=200, value=120)
chol = st.number_input("Colesterol sérico (mg/dl)", min_value=100, max_value=600, value=200)
fbs = st.radio("¿Glucosa en ayunas > 120 mg/dl?", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Sí")
restecg = st.radio("Resultado del electrocardiograma en reposo",
                   options=[0, 1, 2],
                   format_func=lambda x: [
                       "0: Normal",
                       "1: Anomalía de la onda ST-T",
                       "2: Hipertrofia ventricular izquierda"
                   ][x])
thalach = st.number_input("Frecuencia cardíaca máxima alcanzada", min_value=70, max_value=210, value=150)
exang = st.radio("¿Angina inducida por ejercicio?", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Sí")
oldpeak = st.slider("Depresión del ST inducida por ejercicio", 0.0, 6.0, 1.0)
slope = st.radio("Pendiente del segmento ST",
                 options=[0, 1, 2],
                 format_func=lambda x: [
                     "0: Descendente",
                     "1: Plano",
                     "2: Ascendente"
                 ][x])
ca = st.radio("Número de vasos principales coloreados con fluoroscopía",
              options=[0, 1, 2, 3, 4],
              format_func=lambda x: f"{x} vasos")
thal = st.radio("Resultado de la prueba de talasemia",
                options=[0, 1, 2, 3],
                format_func=lambda x: [
                    "0: Desconocido",
                    "1: Normal",
                    "2: Defecto fijo",
                    "3: Defecto reversible"
                ][x])

# Crear DataFrame para predecir
input_data = pd.DataFrame({
    'age': [age],
    'sex': [sex],
    'cp': [int(cp[0])],
    'trestbps': [trestbps],
    'chol': [chol],
    'fbs': [fbs],
    'restecg': [restecg],
    'thalach': [thalach],
    'exang': [exang],
    'oldpeak': [oldpeak],
    'slope': [slope],
    'ca': [ca],
    'thal': [thal[0] if thal != "0: Desconocido" else 0]
})

# Botón para predecir
if st.button("📊 Predecir"):
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        st.success("✅ Riesgo de enfermedad cardíaca detectado. Se recomienda atención médica especializada.")
    else:
        st.info("🫶 No se detecta riesgo significativo de enfermedad cardíaca. Mantener hábitos saludables.")
