import streamlit as st
import numpy as np
import joblib

# Cargar modelo y escalador
model = joblib.load("heart_model.pkl")
scaler = joblib.load("escalador.pkl")

# Configuración de página
st.set_page_config(page_title="Predicción de Enfermedad Cardíaca", layout="centered", page_icon="❤️")

# Título y descripción
st.title("❤️ Predicción de Enfermedad Cardíaca")
st.write("""
Esta aplicación te ayuda a evaluar el riesgo de enfermedad cardíaca con base en tus datos clínicos.  
Por favor, llena el siguiente formulario. Si no entiendes algún término, coloca el cursor sobre el ícono (❓).
""")

# Formulario de ingreso de datos
with st.form("formulario_prediccion"):
    st.header("🩺 Ingresa los datos del paciente:")

    age = st.slider("Edad", 29, 77, help="Edad en años.")

    sex = st.selectbox("Sexo", options=[0, 1], format_func=lambda x: "Mujer" if x == 0 else "Hombre",
                       help="Selecciona el sexo biológico del paciente.")

    cp = st.selectbox("Tipo de dolor en el pecho", options=[0, 1, 2, 3], help="""
**0:** Angina típica  
**1:** Angina atípica  
**2:** Dolor no anginoso  
**3:** Dolor no relacionado al corazón
""")

    trestbps = st.slider("Presión arterial en reposo (mm Hg)", 90, 200, help="Presión arterial sistólica al estar en reposo.")
    chol = st.slider("Colesterol sérico (mg/dl)", 120, 600, help="Nivel total de colesterol en sangre.")
    
    fbs = st.radio("¿Glucosa en ayunas > 120 mg/dl?", options=[1, 0], format_func=lambda x: "Sí" if x == 1 else "No",
                   help="1: Sí, 0: No")

    restecg = st.selectbox("Resultado del electrocardiograma en reposo", options=[0, 1, 2], help="""
**0:** Normal  
**1:** Anormalidad en la onda ST-T  
**2:** Hipertrofia ventricular izquierda
""")

    thalach = st.slider("Frecuencia cardíaca máxima alcanzada", 70, 210, help="Frecuencia máxima lograda durante el ejercicio.")

    exang = st.radio("¿Angina inducida por ejercicio?", options=[1, 0], format_func=lambda x: "Sí" if x == 1 else "No",
                     help="Dolor en el pecho provocado por la actividad física.")

    oldpeak = st.slider("Depresión ST inducida por ejercicio", 0.0, 6.5, step=0.1, help="""
Diferencia entre la línea base y el nivel ST durante el ejercicio.  
Valores mayores pueden indicar isquemia.
""")

    slope = st.selectbox("Pendiente del segmento ST", options=[0, 1, 2], help="""
**0:** Descendente  
**1:** Plana  
**2:** Ascendente
""")

    ca = st.slider("Número de vasos coloreados (fluoroscopía)", 0, 4, help="Cantidad de vasos sanguíneos visibles con medio de contraste.")

    thal = st.selectbox("Resultado del test de talasemia", options=[1, 2, 3], help="""
**1:** Fijo (defecto permanente)  
**2:** Normal  
**3:** Reversible (defecto que mejora con esfuerzo)
""")

    submit = st.form_submit_button("Predecir")

# Procesar predicción
if submit:
    datos_usuario = np.array([[age, sex, cp, trestbps, chol, fbs, restecg,
                               thalach, exang, oldpeak, slope, ca, thal]])
    datos_escalados = scaler.transform(datos_usuario)
    
    prediccion = model.predict(datos_escalados)[0]
    probabilidad = model.predict_proba(datos_escalados)[0][int(prediccion)]

    st.subheader("📊 Resultado del análisis")

    if prediccion == 1:
        st.error("🔴 Posible riesgo de enfermedad cardíaca detectado.")
        st.markdown(f"**Probabilidad estimada:** {probabilidad*100:.2f}%")
        st.info("""
Se recomienda realizar un examen clínico completo.  
Estos podrían incluir: **electrocardiograma**, **ecocardiografía**, **prueba de esfuerzo**, y **análisis de sangre**.
""")
    else:
        st.success("🟢 No se detectan signos significativos de enfermedad cardíaca.")
        st.markdown(f"**Probabilidad estimada de enfermedad:** {probabilidad*100:.2f}%")
        st.info("""
Aunque el modelo no detecta un riesgo elevado, se recomienda mantener hábitos saludables  
y realizar chequeos periódicos si existen antecedentes familiares.
""")

# Footer
st.markdown("---")
st.caption("🧠 Este modelo fue entrenado con datos del conjunto heart-disease y optimizado con Random Forest.")
