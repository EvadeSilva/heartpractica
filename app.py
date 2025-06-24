import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Cargar modelo y escalador
model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")  # Asegúrate de tener este archivo

# Configuración de la página
st.set_page_config(page_title="Predicción de Enfermedad Cardíaca", layout="centered", page_icon="❤️")
st.title("🫀 Predicción de Enfermedad Cardíaca")

st.markdown("""
Esta aplicación permite estimar el **riesgo de enfermedad cardíaca** en base a resultados de exámenes médicos.  
⚠️ *No reemplaza una evaluación médica profesional.*
""")

st.subheader("🔍 Ingresa los datos del paciente:")

# Formulario de entrada con explicaciones
edad = st.slider("Edad", 29, 77, 50, help="Edad del paciente en años.")

sexo = st.selectbox(
    "Sexo", 
    options=["Mujer", "Hombre"],
    help="Sexo del paciente."
)
sexo_val = 0 if sexo == "Mujer" else 1

dolor_pecho = st.selectbox(
    "Tipo de dolor en el pecho", 
    options=[
        "0 - Angina típica",
        "1 - Angina atípica",
        "2 - Dolor no anginoso",
        "3 - Asintomático"
    ],
    help="Tipo de dolor que presenta el paciente."
)
cp_val = int(dolor_pecho[0])

presion = st.slider("Presión arterial en reposo (mm Hg)", 90, 200, 120,
                    help="Presión sanguínea al inicio del examen.")
colesterol = st.slider("Colesterol sérico (mg/dl)", 100, 600, 240,
                       help="Colesterol total. Valores normales suelen estar por debajo de 200.")
azucar = st.radio("¿Azúcar en sangre en ayunas > 120 mg/dl?",
                  options=["No", "Sí"])
fbs_val = 1 if azucar == "Sí" else 0

electro = st.selectbox(
    "Resultados del electrocardiograma en reposo",
    options=[
        "0 - Normal",
        "1 - Anormalidad en la onda ST-T",
        "2 - Hipertrofia ventricular izquierda"
    ],
    help="Resultados del ECG en reposo."
)
restecg_val = int(electro[0])

frecuencia = st.slider("Frecuencia cardíaca máxima alcanzada", 70, 210, 150,
                       help="Frecuencia cardíaca máxima lograda durante el ejercicio.")
angina = st.radio("¿Angina inducida por ejercicio?",
                  options=["No", "Sí"])
exang_val = 1 if angina == "Sí" else 0

oldpeak = st.slider("Depresión ST inducida por ejercicio", 0.0, 6.5, 1.0, step=0.1,
                    help="Diferencia en el segmento ST durante el esfuerzo. Valores altos pueden indicar isquemia.")

pendiente = st.selectbox(
    "Pendiente del segmento ST",
    options=[
        "0 - Ascendente",
        "1 - Plana",
        "2 - Descendente"
    ],
    help="Forma del segmento ST durante el ejercicio."
)
slope_val = int(pendiente[0])

ca = st.slider("Número de vasos coloreados (fluoroscopía)", 0, 4, 0,
               help="Cantidad de vasos sanguíneos observados con tinte.")

talasemia = st.selectbox(
    "Resultado del test de talasemia",
    options=[
        "0 - Normal",
        "1 - Fija",
        "2 - Reversible"
    ],
    help="Tipo de anormalidad en los glóbulos rojos."
)
thal_val = int(talasemia[0])

# Datos del paciente
datos_paciente = np.array([[edad, sexo_val, cp_val, presion, colesterol, fbs_val, restecg_val,
                            frecuencia, exang_val, oldpeak, slope_val, ca, thal_val]])

datos_paciente_esc = scaler.transform(datos_paciente)

if st.button("Predecir"):
    resultado = model.predict(datos_paciente_esc)[0]
    prob = model.predict_proba(datos_paciente_esc)[0][1] * 100

    if resultado == 1:
        st.error(f"❌ El modelo predice que **SÍ hay riesgo de enfermedad cardíaca** con una probabilidad del **{prob:.2f}%**.")
        st.markdown("""
        ### 📌 Recomendaciones generales:
        - Consulta con un cardiólogo.
        - Realiza pruebas adicionales como ecocardiograma, prueba de esfuerzo o angiografía.
        - Mejora hábitos alimenticios y realiza actividad física.
        """)
    else:
        st.success(f"✅ El modelo predice que **NO hay riesgo de enfermedad cardíaca** con una probabilidad del **{100 - prob:.2f}%**.")
        st.markdown("""
        ### 🛡️ Aún así:
        - Mantén controles médicos periódicos.
        - Una vida saludable reduce significativamente el riesgo.
        """)

# Pie de página
st.markdown("---")
st.caption("Este modelo fue entrenado con datos del conjunto [heart-disease] y optimizado con Random Forest.")
