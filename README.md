# ✈️ Proyecto de Predicción de Satisfacción del Cliente de Aerolíneas

## 🎯 Objetivo del Proyecto

El objetivo de este proyecto es desarrollar un modelo de machine learning para predecir la satisfacción de los clientes de una aerolínea en función de varios factores como el servicio a bordo, el confort del asiento, los retrasos en los vuelos, entre otros.

Utilizando datos históricos proporcionados por F5 Airlines, entrenaremos un modelo supervisado de clasificación para identificar qué factores son más importantes para la satisfacción del cliente. Además, hemos desarrollado una aplicación interactiva utilizando Streamlit para predecir la satisfacción de nuevos clientes en tiempo real.

## 📊 Diccionario de Datos

| **Columna**                             | **Tipo de Datos** | **Descripción**                                                                 |
|-----------------------------------------|-------------------|---------------------------------------------------------------------------------|
| Unnamed: 0                              | int64             | Índice de fila que parece no tener un uso particular (puede eliminarse).          |
| id                                      | int64             | Identificador único para cada pasajero.                                           |
| Gender                                  | object            | Género del pasajero (Masculino o Femenino).                                       |
| Customer Type                           | object            | Tipo de cliente: "Loyal Customer" o "disloyal Customer".                          |
| Age                                     | int64             | Edad del pasajero.                                                                |
| Type of Travel                          | object            | Tipo de viaje: "Personal Travel" o "Business travel".                             |
| Class                                   | object            | Clase del asiento del pasajero: "Eco", "Eco Plus", o "Business".                  |
| Flight Distance                         | int64             | Distancia del vuelo en millas.                                                   |
| Inflight wifi service                   | int64             | Nivel de satisfacción con el servicio de wifi a bordo (escala de 1 a 5).           |
| Departure/Arrival time convenient       | int64             | Conveniencia del tiempo de salida/llegada (escala de 1 a 5).                      |
| Ease of Online booking                  | int64             | Facilidad para hacer reservas en línea (escala de 1 a 5).                         |
| Gate location                           | int64             | Satisfacción con la ubicación de la puerta de embarque (escala de 1 a 5).         |
| Food and drink                          | int64             | Satisfacción con la comida y bebida (escala de 1 a 5).                            |
| Online boarding                         | int64             | Satisfacción con el proceso de embarque en línea (escala de 1 a 5).               |
| Seat comfort                            | int64             | Satisfacción con la comodidad del asiento (escala de 1 a 5).                      |
| Inflight entertainment                  | int64             | Satisfacción con el entretenimiento a bordo (escala de 1 a 5).                    |
| On-board service                        | int64             | Satisfacción con el servicio a bordo (escala de 1 a 5).                           |
| Leg room service                        | int64             | Satisfacción con el espacio para las piernas (escala de 1 a 5).                   |
| Baggage handling                        | int64             | Satisfacción con la manipulación del equipaje (escala de 1 a 5).                  |
| Checkin service                         | int64             | Satisfacción con el servicio de check-in (escala de 1 a 5).                       |
| Inflight service                        | int64             | Satisfacción con el servicio en vuelo (escala de 1 a 5).                          |
| Cleanliness                             | int64             | Satisfacción con la limpieza (escala de 1 a 5).                                   |
| Departure Delay in Minutes              | int64             | Minutos de retraso en la salida.                                                 |
| Arrival Delay in Minutes                | float64           | Minutos de retraso en la llegada (tiene algunos valores faltantes).               |
| satisfaction                            | object            | Satisfacción del cliente: "satisfied" o "neutral or dissatisfied".                 |

## 🚀 Instrucciones para la Ejecución

### 1. Configuración de la Base de Datos

El proyecto utiliza una base de datos SQLite para almacenar los datos de entrenamiento y prueba. Para configurar SQLite en tu máquina Windows:

1. **Descarga SQLite**: Visita la página oficial de [SQLite](https://www.sqlite.org/download.html) y descarga el archivo ZIP de herramientas de línea de comandos para Windows.

2. **Instala SQLite**:
   - Extrae el contenido del archivo ZIP descargado en una carpeta de tu elección, por ejemplo, `C:\sqlite`.
   - Copia la ruta de la carpeta `C:\sqlite`.

3. **Configura la Variable de Entorno**:
   - Abre el Panel de Control y navega a `Sistema y Seguridad` > `Sistema` > `Configuración avanzada del sistema`.
   - En la ventana de Propiedades del Sistema, haz clic en `Variables de entorno...`.
   - En la sección de Variables del sistema, selecciona la variable `Path` y haz clic en `Editar...`.
   - Agrega la ruta `C:\sqlite` a la lista de valores y guarda los cambios.

4. **Verifica la instalación**: Abre una terminal de comandos (CMD) y escribe `sqlite3`. Si todo está configurado correctamente, deberías ver la consola de SQLite.

### 2. Configuración del Entorno de Desarrollo

- **Instala las dependencias**:
  ```bash
  pip install -r requirements.txt
  ```

### 3. Ejecución de la Aplicación Streamlit

La aplicación utiliza Streamlit para proporcionar una interfaz interactiva para predecir la satisfacción del cliente.

- **Inicia la aplicación**:
  ```bash
  streamlit run streamlit_app/app.py
  ```

### 4. Algoritmo Implementado en la Aplicación

La aplicación de Streamlit utiliza un modelo de **CatBoostClassifier** para predecir la satisfacción del cliente. Este modelo es un algoritmo de boosting de gradiente que maneja eficientemente datos categóricos y es robusto frente a datos faltantes.

#### Funcionalidades de la Aplicación:

- **Carga de datos**: Permite al usuario cargar datos nuevos para realizar predicciones.
- **Predicción en tiempo real**: Realiza predicciones de satisfacción del cliente basado en los datos de entrada proporcionados.
- **Visualización de resultados**: Muestra los resultados de las predicciones junto con métricas de evaluación como la precisión y la matriz de confusión.

## 📁 Estructura del Proyecto

```
G1_ML_Airline/
├── data/
│   ├── database/
│   │   └── airline_satisfaction.db
│   ├── airline_passenger_satisfaction.csv
├── logs/
├── modelos_entrenamiento/
│   ├── catboost_model.cbm
│   ├── X_test.csv
│   ├── X_train.csv
│   ├── X_val.csv
│   ├── y_test.csv
│   ├── y_train.csv
│   ├── y_val.csv
├── modelos/
│   ├── catboost_info/
│   ├── arboles_decision.ipynb
│   ├── gradient_boosting.ipynb
│   ├── random_forest.ipynb
│   ├── regresion_lineal_multiple.ipynb
│   ├── regresion_lineal_simple.ipynb
│   ├── regresion_logistica.ipynb
│   ├── separar_dataset.ipynb
│   ├── XGBoost.ipynb
├── notebooks/
│   ├── analisis_datos.ipynb
│   └── tratamiento_datos.ipynb
├── streamlit_app/
│   ├── __pycache__/
│   ├── images/
│   ├── app.py
│   ├── config.py
│   ├── initialize_db.py
├── LICENSE
├── README.md
└── requirements.txt
```

## 🛠️ Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal utilizado para el desarrollo del modelo y la aplicación.
- **Pandas**: Biblioteca utilizada para la manipulación y análisis de datos.
- **Scikit-learn**: Biblioteca para la implementación de algoritmos de machine learning.
- **Streamlit**: Plataforma utilizada para construir la aplicación web interactiva.
- **Matplotlib/Seaborn**: Bibliotecas utilizadas para la visualización de datos.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

Agradecemos a todos los miembros del equipo y a nuestros instructores por su apoyo y orientación en el desarrollo de este proyecto.

## ⚠️ Reminder para Aitor

Reflejar el nivel de los objetivos que se propone alcanzar el grupo de alumnos con el desarrollo del proyecto, y motivarlo en base a las circunstancias personales de sus miembros.

Presentar a los miembros del equipo así como los roles que ha desempeñado en el desarrollo.
