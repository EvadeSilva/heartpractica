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

# Diccionarios explicativos
sex_dict = {"Femenino": 0, "Masculino": 1}
cp_dict = {
    "Angina típica": 0,
    "Angina atípica": 1,
    "Dolor no anginoso": 2,
    "Dolor no relacionado al corazón": 3
}
restecg_dict = {
    "Normal": 0,
    "Anormalidad en la onda ST-T": 1,
    "Hipertrofia ventricular izquierda": 2
}
slope_dict = {
    "Descendente": 0,
    "Plana": 1,
    "Ascendente": 2
}
thal_dict = {
    "Fijo (defecto permanente)": 1,
    "Normal": 2,
    "Reversible (mejora con esfuerzo)": 3
}

# Formulario de ingreso de datos
with st.form("formulario_prediccion"):
    st.header("🩺 Ingresa los datos del paciente:")

    age = st.slider("Edad", 29, 77, help="Edad en años.")

    sex_label = st.selectbox("Sexo", options=list(sex_dict.keys()), help="Sexo biológico del paciente.")
    sex = sex_dict[sex_label]

    cp_label = st.selectbox("Tipo de dolor en el pecho", options=list(cp_dict.keys()), help="""
    - Angina típica: Dolor en el pecho relacionado al esfuerzo físico.
    - Angina atípica: Dolor con características no clásicas.
    - Dolor no anginoso: Dolor torácico no relacionado con el corazón.
    - Dolor no relacionado al corazón: Otra causa no cardíaca.
    """)
    cp = cp_dict[cp_label]

    trestbps = st.slider("Presión arterial en reposo (mm Hg)", 90, 200, help="Presión arterial sistólica al estar en reposo.")
    chol = st.slider("Colesterol sérico (mg/dl)", 120, 600, help="Nivel total de colesterol en sangre.")

    fbs = st.radio("¿Glucosa en ayunas > 120 mg/dl?", options=["Sí", "No"], help="Indica si el nivel de glucosa en ayunas supera los 120 mg/dl.")
    fbs = 1 if fbs == "Sí" else 0

    restecg_label = st.selectbox("Resultado del electrocardiograma en reposo", options=list(restecg_dict.keys()), help="""
    - Normal
    - Anormalidad en la onda ST-T: Cambios que pueden indicar isquemia.
    - Hipertrofia ventricular izquierda: Aumento del tamaño del músculo cardíaco.
    """)
    restecg = restecg_dict[restecg_label]

    thalach = st.slider("Frecuencia cardíaca máxima alcanzada", 70, 210, help="Frecuencia máxima lograda durante el ejercicio.")

    exang = st.radio("¿Angina inducida por ejercicio?", options=["Sí", "No"], help="Dolor en el pecho provocado por la actividad física.")
    exang = 1 if exang == "Sí" else 0

    oldpeak = st.slider("Depresión del ST inducida por ejercicio (mm)", 0.0, 6.5, step=0.1, help="""
    Depresión ST: Diferencia entre la línea base y el segmento ST durante el esfuerzo.  
    Valores altos pueden sugerir isquemia (falta de oxígeno en el corazón).
    """)

    slope_label = st.selectbox("Pendiente del segmento ST", options=list(slope_dict.keys()), help="""
    - Descendente: Indica empeoramiento durante esfuerzo.
    - Plana: Poco cambio en el ST.
    - Ascendente: Cambio normal tras el ejercicio.
    """)
    slope = slope_dict[slope_label]

    ca = st.slider("Número de vasos coloreados (fluoroscopía)", 0, 4, help="Cantidad de vasos sanguíneos visibles con medio de contraste.")

    thal_label = st.selectbox("Resultado del test de talasemia", options=list(thal_dict.keys()), help="""
    - Fijo: Daño permanente detectado en imagen.
    - Normal: No se detectan anomalías.
    - Reversible: Se observa mejora con ejercicio.
    """)
    thal = thal_dict[thal_label]

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
