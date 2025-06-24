import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar modelo y escalador
model = joblib.load("heart_model.pkl")
scaler = joblib.load("escalador.pkl")

# Título
st.title("🫀 Predicción de Enfermedad Cardíaca")
st.markdown("""
Esta aplicación permite estimar la probabilidad de enfermedad cardíaca en función de diversos parámetros clínicos.  
A continuación se presentan definiciones breves de los términos utilizados:

### 🧠 Glosario rápido:
- **cp (Chest Pain - Dolor en el pecho)**  
    - `0`: Asintomático  
    - `1`: Angina típica  
    - `2`: Angina atípica  
    - `3`: Dolor no anginal  

- **restecg (Electrocardiograma en reposo)**  
    - `0`: Normal  
    - `1`: Anormalidad ST-T (inversión T, elevación ST)  
    - `2`: Hipertrofia ventricular izquierda  

- **slope (Pendiente del segmento ST durante el ejercicio)**  
    - `0`: Descendente  
    - `1`: Plana  
    - `2`: Ascendente  

- **thal (Talassemia)**  
    - `0`: No disponible  
    - `1`: Talasemia fija (defecto irreversible)  
    - `2`: Normal  
    - `3`: Talasemia reversible (bajo estrés)  

- **oldpeak**: Depresión del segmento ST inducida por el ejercicio en relación al reposo.

""")

# Formulario de ingreso de datos
st.header("📋 Ingrese los datos del paciente:")

age = st.slider("Edad", 29, 77, 50)
sex = st.selectbox("Sexo", [("Hombre", 1), ("Mujer", 0)], format_func=lambda x: x[0])[1]
cp = st.selectbox("Tipo de dolor en el pecho", [
    ("Asintomático", 0),
    ("Angina típica", 1),
    ("Angina atípica", 2),
    ("Dolor no anginal", 3)
], format_func=lambda x: x[0])[1]

trestbps = st.slider("Presión arterial en reposo (mm Hg)", 90, 200, 120)
chol = st.slider("Colesterol sérico (mg/dl)", 100, 600, 200)
fbs = st.selectbox("¿Glucosa en ayunas > 120 mg/dl?", [("Sí", 1), ("No", 0)], format_func=lambda x: x[0])[1]
restecg = st.selectbox("Resultado del electrocardiograma en reposo", [
    ("Normal", 0),
    ("Anormalidad ST-T", 1),
    ("Hipertrofia ventricular izquierda", 2)
], format_func=lambda x: x[0])[1]

thalach = st.slider("Frecuencia cardíaca máxima alcanzada", 70, 210, 150)
exang = st.selectbox("¿Angina inducida por ejercicio?", [("Sí", 1), ("No", 0)], format_func=lambda x: x[0])[1]
oldpeak = st.slider("Oldpeak (depresión ST)", 0.0, 6.2, 1.0)
slope = st.selectbox("Pendiente del segmento ST", [
    ("Descendente", 0),
    ("Plana", 1),
    ("Ascendente", 2)
], format_func=lambda x: x[0])[1]

ca = st.slider("Número de vasos principales con fluoroscopía (0–3)", 0, 3, 0)
thal = st.selectbox("Resultado del test de talasemia", [
    ("No disponible", 0),
    ("Fijo", 1),
    ("Normal", 2),
    ("Reversible", 3)
], format_func=lambda x: x[0])[1]

# Botón de predicción
if st.button("🧾 Evaluar Riesgo Cardíaco"):
    input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg,
                            thalach, exang, oldpeak, slope, ca, thal]])
    
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0][1]

    if prediction == 1:
        st.error(f"🔴 El modelo predice **presencia de enfermedad cardíaca** con una probabilidad de {probability:.2%}.")
        st.markdown("""
        ### 🧬 Recomendaciones sugeridas:
        - Consulta médica urgente con un cardiólogo.
        - Evaluación con pruebas como ecocardiograma, prueba de esfuerzo o angiografía coronaria.
        - Cambios en el estilo de vida: dieta, ejercicio y control del estrés.

        """)
    else:
        st.success(f"🟢 El modelo predice **ausencia de enfermedad cardíaca** con una probabilidad de {(1 - probability):.2%}.")
        st.markdown("""
        ### ✅ Recomendaciones sugeridas:
        - Mantener hábitos saludables.
        - Revisiones periódicas.
        - Continuar monitoreando factores de riesgo si existen antecedentes familiares.

        """)

# Pie de página
st.markdown("---")
st.caption("📊 Basado en modelo Random Forest entrenado con el dataset 'heart-disease'. Esta herramienta no reemplaza una evaluación médica profesional.")
