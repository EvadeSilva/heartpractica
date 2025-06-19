# app.py  ─────────  aplicación Streamlit para predicción de enfermedad cardíaca
import streamlit as st
import numpy as np
import joblib

st.set_page_config(page_title="Predicción Enfermedad Cardíaca", layout="centered")
st.title("💓 Predicción de Enfermedad Cardíaca (Dataset UCI)")

# -----------------------------------------------------------
# 1) Cargar el modelo entrenado (pipeline completo)
# -----------------------------------------------------------
MODEL_PATH = "heart_model_tuned.pkl"
model = joblib.load(MODEL_PATH)

# Orden exacta de features que espera el pipeline
FEATURES = [
    "age", "trestbps", "chol", "thalach", "oldpeak",  # numéricas
    "sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"  # categóricas
]

# -----------------------------------------------------------
# 2) Obtener los datos del usuario
# -----------------------------------------------------------
st.sidebar.header("Ingrese los datos del paciente")

def user_inputs():
    # inputs numéricos
    age      = st.sidebar.number_input("Edad (años)",         29, 77, 55)
    trestbps = st.sidebar.number_input("Presión en reposo",   80, 200, 120)
    chol     = st.sidebar.number_input("Colesterol (mg/dl)",  100, 600, 240)
    thalach  = st.sidebar.number_input("FC máxima",           70, 210, 150)
    oldpeak  = st.sidebar.number_input("OLDPEAK",             0.0, 6.0, 1.0, step=0.1)

    # inputs categóricos (mismos valores que en entrenamiento)
    sex   = st.sidebar.selectbox("Sexo (1=Hombre, 0=Mujer)",      [1, 0])
    cp    = st.sidebar.selectbox("Dolor pecho (0–3)",             [0, 1, 2, 3])
    fbs   = st.sidebar.selectbox("FBS >120 mg/dl (1=Sí, 0=No)",   [1, 0])
    restecg = st.sidebar.selectbox("RestECG (0–2)",              [0, 1, 2])
    exang   = st.sidebar.selectbox("Angina ejercicio (1=Sí,0=No)",[1, 0])
    slope   = st.sidebar.selectbox("Pendiente ST (0–2)",          [0, 1, 2])
    ca      = st.sidebar.selectbox("Vasos coloreados (0–4)",      [0, 1, 2, 3, 4])
    thal    = st.sidebar.selectbox("Thal (0=normal,1=fijo,2=rev)",[0, 1, 2])

    # Mantener el orden de FEATURES
    inputs = np.array([[age, trestbps, chol, thalach, oldpeak,
                        sex, cp, fbs, restecg, exang, slope, ca, thal]])

    return
