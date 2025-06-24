import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar modelo
model = joblib.load("heart_model_rf.pkl")

# Título
st.title("Predicción de Enfermedad Cardíaca")
st.markdown("Esta aplicación predice la **probabilidad de enfermedad cardíaca** basándose en parámetros médicos. No reemplaza una consulta médica.")

# Opciones explicadas
cp_dict = {
    "Dolor típico anginoso": 0,
    "Dolor atípico anginoso": 1,
    "Dolor no anginoso": 2,
    "Asintomático": 3
}
restecg_dict = {
    "Normal": 0,
    "Anormalidad ST-T (ondas T invertidas o elevación ST >0.05 mV)": 1,
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

# Formulario de entrada
with st.form("input_form"):
    age = st.slider("Edad", 29, 77, 50)
    sex = st.radio("Sexo", ["Hombre", "Mujer"])
    cp = st.selectbox("Tipo de dolor en el pecho", list(cp_dict.keys()))
    trestbps = st.slider("Presión arterial en reposo (mm Hg)", 80, 200, 120)
    chol = st.sli
