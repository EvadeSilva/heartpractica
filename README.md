📌 Descripción del Proyecto
Este proyecto utiliza técnicas de aprendizaje automático para predecir el riesgo de enfermedad cardíaca a partir de datos clínicos. Se entrenó un modelo de clasificación con el algoritmo Random Forest, empleando un conjunto de datos público de pacientes.

La aplicación final permite que el usuario ingrese sus datos clínicos y obtenga una estimación del riesgo, junto con recomendaciones generales. Está desplegada en Streamlit Cloud para su uso interactivo.

🎯 Objetivos
Realizar análisis exploratorio y procesamiento de datos clínicos.

Entrenar y evaluar un modelo de clasificación.

Implementar una interfaz amigable para usuarios no especializados en medicina o ciencia de datos.

Facilitar el uso del modelo para fines educativos y de concienciación.

🗂️ Estructura del Repositorio
bash
Copiar
Editar
heart-disease-predictor/
│
├── app.py                       # Código de la aplicación Streamlit
├── heart_model.pkl             # Modelo entrenado (Random Forest)
├── escalador.pkl               # Escalador de características (StandardScaler)
├── heart.csv                   # Dataset original (si no se carga desde OpenML)
├── Proyecto Final 2 ML.ipynb   # Cuaderno con el análisis exploratorio y entrenamiento
├── requirements.txt            # Lista de dependencias para reproducir el proyecto
└── README.md                   # Este archivo de documentación
📊 Dataset
Fuente: Heart Disease Dataset – UCI / OpenML

Variables clínicas incluidas:

Edad, sexo, tipo de dolor en el pecho, presión arterial, colesterol, glucosa en ayunas, resultados de ECG, frecuencia cardíaca máxima, angina inducida por ejercicio, depresión ST, talasemia, entre otras.

📈 Proceso de Desarrollo
Análisis exploratorio de datos (EDA):

Visualización de distribuciones y correlaciones.

Revisión de valores atípicos y distribución por clase.

Preprocesamiento:

Conversión de variables categóricas.

Estandarización de características numéricas.

Entrenamiento del modelo:

División entrenamiento/prueba.

Uso de RandomForestClassifier.

Evaluación con precisión, recall y F1-score.

Despliegue:

App desarrollada con Streamlit.

Interfaz diseñada para usuarios sin conocimientos técnicos.


🌐 Aplicación en línea
Puedes probar la app aquí: https://heartpractica-6vcy6zvcvdxpqbjua7nop9.streamlit.app

📚 Glosario y Explicaciones
La app incluye explicaciones breves en cada campo sobre:

Dolores en el pecho: desde anginosos típicos hasta asintomáticos.

Depresión ST: indicadores de isquemia.

Talasemia: defectos sanguíneos que pueden afectar el corazón.

Valores normales: presión arterial, colesterol, frecuencia cardíaca, etc.

💡 Resultados
El modelo alcanzó una precisión de aproximadamente  8%% en el conjunto de prueba, lo que demuestra su potencial para identificar casos de riesgo.

⚠️ Aviso importante
Esta herramienta no sustituye una consulta médica profesional. Está diseñada con fines educativos y de orientación general. Ante cualquier síntoma, consulta a tu médico.

👥 Autores
Nombre ZAHID SILVA 
       Y CHAT GPT MAS CONOCIDO COMO "ISAAC"






