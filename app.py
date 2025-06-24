import streamlit as st
import pandas as pd
import joblib

# Título
st.title("🫀 Predicción de enfermedad cardíaca")

# Cargar modelo
@st.cache(allow_output_mutation=True)
def load_model():
    return joblib.load("heart_model.pkl")

model = load_model()

# Interfaz
st.subheader("🔍 Ingresa los datos del paciente:")

age = st.slider("Edad", 29, 77, 50)
sex = st.selectbox("Sexo (0: Mujer, 1: Hombre)", [0, 1])
cp = st.selectbox("Tipo de dolor en el pecho (0-3)", [0, 1, 2, 3])
trestbps = st.number_input("Presión arterial en reposo", min_value=90, max_value=200, value=120)
chol = st.number_input("Colesterol sérico", min_value=100, max_value=600, value=200)
fbs = st.selectbox("Azúcar en sangre en ayunas > 120 mg/dl (1: Sí, 0: No)", [0, 1])
restecg = st.selectbox("Resultados del electrocardiograma", [0, 1, 2])
thalach = st.number_input("Frecuencia cardíaca máxima alcanzada", min_value=70, max_value=210, value=150)
exang = st.selectbox("Angina inducida por ejercicio (1: Sí, 0: No)", [0, 1])
oldpeak = st.slider("Depresión inducida por ejercicio", 0.0, 6.0, 1.0)
slope = st.selectbox("Pendiente del segmento ST", [0, 1, 2])
ca = st.selectbox("Número de vasos coloreados con fluoroscopía (0-4)", [0, 1, 2, 3, 4])
thal = st.selectbox("Talasemia (1 = normal; 2 = defecto fijo; 3 = defecto reversible)", [0, 1, 2, 3])

# Crear DataFrame para predecir
input_data = pd.DataFrame({
    'age': [age],
    'sex': [sex],
    'cp': [cp],
    'trestbps': [trestbps],
    'chol': [chol],
    'fbs': [fbs],
    'restecg': [restecg],
    'thalach': [thalach],
    'exang': [exang],
    'oldpeak': [oldpeak],
    'slope': [slope],
    'ca': [ca],
    'thal': [thal]
})

# Botón para predecir
if st.button("📊 Predecir"):
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        st.success("✅ Riesgo de enfermedad cardíaca detectado.")
    else:
        st.info("🫶 No se detecta riesgo de enfermedad cardíaca.")

