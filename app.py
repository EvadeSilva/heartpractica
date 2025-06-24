# Formulario para ingresar los datos del paciente
st.sidebar.header("🔍 Ingresa los datos del paciente")

age = st.sidebar.number_input("Edad (en años)", min_value=1, max_value=120,
                              help="Edad de la persona. Ejemplo: 45")

sex = st.sidebar.selectbox("Sexo", options=[0, 1],
                           format_func=lambda x: "Mujer" if x == 0 else "Hombre",
                           help="Selecciona 0 si es Mujer, 1 si es Hombre.")

cp = st.sidebar.selectbox("Tipo de dolor en el pecho", options=[0, 1, 2, 3],
                          format_func=lambda x: [
                              "0 - Dolor típico anginoso (relacionado al esfuerzo físico)",
                              "1 - Dolor atípico anginoso",
                              "2 - Dolor no anginoso",
                              "3 - Dolor sin relación con el corazón"
                          ][x],
                          help="Tipo de dolor que presenta el paciente.")

trestbps = st.sidebar.number_input("Presión arterial en reposo (mm Hg)", min_value=50, max_value=250,
                                   help="Presión sistólica medida en reposo. Normal: 90–120 mm Hg.")

chol = st.sidebar.number_input("Colesterol sérico (mg/dl)", min_value=100, max_value=600,
                               help="Nivel de colesterol total en sangre. Normal: menos de 200 mg/dl.")

fbs = st.sidebar.selectbox("¿Glucosa en ayunas > 120 mg/dl?", options=[0, 1],
                           format_func=lambda x: "No" if x == 0 else "Sí",
                           help="Indica si la glucosa en ayunas supera los 120 mg/dl.")

restecg = st.sidebar.selectbox("Resultado del ECG en reposo", options=[0, 1, 2],
                               format_func=lambda x: [
                                   "0 - Normal",
                                   "1 - Anomalía en ST-T (posible isquemia)",
                                   "2 - Hipertrofia ventricular izquierda"
                               ][x],
                               help="Resultados del electrocardiograma en reposo.")

thalach = st.sidebar.number_input("Frecuencia cardíaca máxima alcanzada", min_value=60, max_value=250,
                                  help="Frecuencia máxima durante esfuerzo. Normal: entre 100 y 190 bpm en adultos.")

exang = st.sidebar.selectbox("¿Presenta angina inducida por ejercicio?", options=[0, 1],
                             format_func=lambda x: "No" if x == 0 else "Sí",
                             help="Angina provocada por actividad física.")

oldpeak = st.sidebar.number_input("Depresión del segmento ST inducida por ejercicio", min_value=0.0, max_value=10.0, step=0.1,
                                  help="Valor numérico que indica la depresión del ST. Una depresión mayor puede ser señal de enfermedad cardíaca.")

slope = st.sidebar.selectbox("Pendiente del ST durante el ejercicio", options=[0, 1, 2],
                             format_func=lambda x: [
                                 "0 - Descendente",
                                 "1 - Plana",
                                 "2 - Ascendente"
                             ][x],
                             help="Pendiente de recuperación del segmento ST durante el esfuerzo.")

ca = st.sidebar.selectbox("Número de vasos principales vistos con fluoroscopía", options=[0, 1, 2, 3, 4],
                          help="Cantidad de vasos sanguíneos visibles mediante fluoroscopía. Mayor número puede indicar mayor riesgo.")

thal = st.sidebar.selectbox("Tipo de talasemia", options=[1, 2, 3],
                            format_func=lambda x: {
                                1: "1 - Sin información",
                                2: "2 - Talasemia normal",
                                3: "3 - Talasemia reversible"
                            }[x],
                            help="Tipo de talasemia detectada en el paciente.")

