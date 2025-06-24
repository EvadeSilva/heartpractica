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
    help="Presión normal: <120 mm Hg. Ma
