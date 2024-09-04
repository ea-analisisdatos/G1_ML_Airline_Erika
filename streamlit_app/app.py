import streamlit as st
import pandas as pd
import sqlite3
from catboost import CatBoostClassifier
from pathlib import Path
from sklearn.metrics import accuracy_score, recall_score, f1_score, roc_auc_score
from config import DB_NAME

# Paleta de colores
PRIMARY_COLOR = "#004687"  # Azul oscuro
SECONDARY_COLOR = "#C8102E"  # Rojo
BACKGROUND_COLOR = "#FFFFFF"  # Blanco
SIDEBAR_BACKGROUND = "#D9D9D9"  # Gris claro
ACCENT_COLOR = "#FFB81C"  # Amarillo dorado

# Ruta del modelo y de las imágenes
MODEL_PATH = Path(__file__).resolve().parent.parent / 'data' / 'modelos_entrenamiento' / 'catboost_model.cbm'
HAPPY_IMAGE_PATH = str(Path(__file__).resolve().parent / 'images' / 'happy_image.png')  # Convertimos a str
SAD_IMAGE_PATH = str(Path(__file__).resolve().parent / 'images' / 'sad_image.png')  # Convertimos a str
FAVICON_PATH = "✈️"  # Usa el emoji de avión directamente

# Configurar el favicon y la página
st.set_page_config(page_title="Encuesta de Satisfacción de Pasajeros", page_icon=FAVICON_PATH, layout="wide")

# Cargar el modelo previamente entrenado
model = CatBoostClassifier()
try:
    model.load_model(str(MODEL_PATH))
except Exception as e:
    st.error(f"Error al cargar el modelo: {e}")
    st.stop()

def connect_db():
    """Conectar a la base de datos SQLite3"""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Exception as e:
        st.error(f"Error de conexión a la base de datos: {e}")
        return None

def insert_passenger(data, satisfaction_predicted):
    """Función para insertar datos en la base de datos, incluyendo la predicción de satisfacción"""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = '''
            INSERT INTO pasajeros (gender, customer_type, age, type_of_travel, seat_class, flight_distance, 
                                   inflight_wifi_service, departure_arrival_time_convenient, ease_of_online_booking, 
                                   gate_location, food_and_drink, online_boarding, seat_comfort, inflight_entertainment, 
                                   on_board_service, leg_room_service, baggage_handling, checkin_service, inflight_service, 
                                   cleanliness, departure_delay_in_minutes, arrival_delay_in_minutes, satisfaction, satisfaction_predicted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, data + [None, satisfaction_predicted])  
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except Exception as e:
            st.error(f"Error al insertar datos en la base de datos: {e}")
            return None

def predict_satisfaction(data):
    """Función para predecir la satisfacción del pasajero"""
    
    # Convertir datos categóricos a números
    categorical_mapping = {
        "gender": {"Male": 0, "Female": 1},
        "customer_type": {"Loyal Customer": 0, "Disloyal Customer": 1},
        "type_of_travel": {"Personal Travel": 0, "Business travel": 1},
        "seat_class": {"Eco": 0, "Eco Plus": 1, "Business": 2}
    }
    
    # Reemplazar valores categóricos con sus correspondientes numéricos
    data[0] = categorical_mapping["gender"][data[0]]
    data[1] = categorical_mapping["customer_type"][data[1]]
    data[3] = categorical_mapping["type_of_travel"][data[3]]
    data[4] = categorical_mapping["seat_class"][data[4]]
    
    # Crear DataFrame con los nombres de columnas correctos
    features = pd.DataFrame([data], columns=[
        "Gender", "Customer Type", "Age", "Type of Travel", "Class", "Flight Distance",
        "Inflight wifi service", "Departure/Arrival time convenient", "Ease of Online booking", 
        "Gate location", "Food and drink", "Online boarding", "Seat comfort", "Inflight entertainment", 
        "On-board service", "Leg room service", "Baggage handling", "Checkin service", "Inflight service", 
        "Cleanliness", "Departure Delay in Minutes", "Arrival Delay in Minutes"
    ])
    
    try:
        prediction = model.predict(features)
        return "Satisfied" if prediction[0] == 1 else "Neutral or Dissatisfied"
    except Exception as e:
        st.error(f"Error al predecir la satisfacción: {e}")
        return None

def main():
    st.title("Formulario de Encuesta de Satisfacción de Pasajeros")

    # Inicializar el estado del formulario si no existe
    if 'form_submitted' not in st.session_state:
        st.session_state['form_submitted'] = False
        st.session_state['gender'] = "Seleccionar"
        st.session_state['customer_type'] = "Seleccionar"
        st.session_state['age'] = 0
        st.session_state['type_of_travel'] = "Seleccionar"
        st.session_state['seat_class'] = "Seleccionar"
        st.session_state['flight_distance'] = 0
        st.session_state['inflight_wifi_service'] = 0
        st.session_state['departure_arrival_time_convenient'] = 0
        st.session_state['ease_of_online_booking'] = 0
        st.session_state['gate_location'] = 0
        st.session_state['food_and_drink'] = 0
        st.session_state['online_boarding'] = 0
        st.session_state['seat_comfort'] = 0
        st.session_state['inflight_entertainment'] = 0
        st.session_state['on_board_service'] = 0
        st.session_state['leg_room_service'] = 0
        st.session_state['baggage_handling'] = 0
        st.session_state['checkin_service'] = 0
        st.session_state['inflight_service'] = 0
        st.session_state['cleanliness'] = 0
        st.session_state['departure_delay_in_minutes'] = 0
        st.session_state['arrival_delay_in_minutes'] = 0
    
    # Barra lateral para los campos del formulario
    with st.sidebar:
        st.header("Rellena la encuesta")

        st.session_state['gender'] = st.selectbox("Gender", ["Seleccionar", "Male", "Female"], index=["Seleccionar", "Male", "Female"].index(st.session_state['gender']))
        st.session_state['customer_type'] = st.selectbox("Customer Type", ["Seleccionar", "Loyal Customer", "Disloyal Customer"], index=["Seleccionar", "Loyal Customer", "Disloyal Customer"].index(st.session_state['customer_type']))
        st.session_state['age'] = st.number_input("Age", min_value=0, max_value=100, step=1, value=st.session_state['age'])
        st.session_state['type_of_travel'] = st.selectbox("Type of Travel", ["Seleccionar", "Personal Travel", "Business travel"], index=["Seleccionar", "Personal Travel", "Business travel"].index(st.session_state['type_of_travel']))
        st.session_state['seat_class'] = st.selectbox("Class", ["Seleccionar", "Eco", "Eco Plus", "Business"], index=["Seleccionar", "Eco", "Eco Plus", "Business"].index(st.session_state['seat_class']))
        st.session_state['flight_distance'] = st.number_input("Flight Distance", min_value=0, max_value=10000, step=1, value=st.session_state['flight_distance'])
        st.session_state['inflight_wifi_service'] = st.slider("Inflight wifi service", 0, 5, value=st.session_state['inflight_wifi_service'])
        st.session_state['departure_arrival_time_convenient'] = st.slider("Departure/Arrival time convenient", 0, 5, value=st.session_state['departure_arrival_time_convenient'])
        st.session_state['ease_of_online_booking'] = st.slider("Ease of Online booking", 0, 5, value=st.session_state['ease_of_online_booking'])
        st.session_state['gate_location'] = st.slider("Gate location", 0, 5, value=st.session_state['gate_location'])
        st.session_state['food_and_drink'] = st.slider("Food and drink", 0, 5, value=st.session_state['food_and_drink'])
        st.session_state['online_boarding'] = st.slider("Online boarding", 0, 5, value=st.session_state['online_boarding'])
        st.session_state['seat_comfort'] = st.slider("Seat comfort", 0, 5, value=st.session_state['seat_comfort'])
        st.session_state['inflight_entertainment'] = st.slider("Inflight entertainment", 0, 5, value=st.session_state['inflight_entertainment'])
        st.session_state['on_board_service'] = st.slider("On-board service", 0, 5, value=st.session_state['on_board_service'])
        st.session_state['leg_room_service'] = st.slider("Leg room service", 0, 5, value=st.session_state['leg_room_service'])
        st.session_state['baggage_handling'] = st.slider("Baggage handling", 0, 5, value=st.session_state['baggage_handling'])
        st.session_state['checkin_service'] = st.slider("Checkin service", 0, 5, value=st.session_state['checkin_service'])
        st.session_state['inflight_service'] = st.slider("Inflight service", 0, 5, value=st.session_state['inflight_service'])
        st.session_state['cleanliness'] = st.slider("Cleanliness", 0, 5, value=st.session_state['cleanliness'])
        st.session_state['departure_delay_in_minutes'] = st.number_input("Departure Delay in Minutes", min_value=0, max_value=10000, step=1, value=st.session_state['departure_delay_in_minutes'])
        st.session_state['arrival_delay_in_minutes'] = st.number_input("Arrival Delay in Minutes", min_value=0, max_value=10000, step=1, value=st.session_state['arrival_delay_in_minutes'])

    # Acción al presionar "Registrar y Predecir Satisfacción"
    if st.sidebar.button("Registrar y Predecir Satisfacción"):
        # Validar que se hayan completado los campos obligatorios
        if (st.session_state['gender'] == "Seleccionar" or 
            st.session_state['customer_type'] == "Seleccionar" or 
            st.session_state['type_of_travel'] == "Seleccionar" or 
            st.session_state['seat_class'] == "Seleccionar"):
            st.warning("Por favor, completa todos los campos obligatorios antes de continuar.")
        else:
            data = [
                st.session_state['gender'], st.session_state['customer_type'], st.session_state['age'],
                st.session_state['type_of_travel'], st.session_state['seat_class'], st.session_state['flight_distance'],
                st.session_state['inflight_wifi_service'], st.session_state['departure_arrival_time_convenient'], 
                st.session_state['ease_of_online_booking'], st.session_state['gate_location'],
                st.session_state['food_and_drink'], st.session_state['online_boarding'], st.session_state['seat_comfort'], 
                st.session_state['inflight_entertainment'], st.session_state['on_board_service'],
                st.session_state['leg_room_service'], st.session_state['baggage_handling'], st.session_state['checkin_service'], 
                st.session_state['inflight_service'], st.session_state['cleanliness'],
                st.session_state['departure_delay_in_minutes'], st.session_state['arrival_delay_in_minutes']
            ]
            
            prediction = predict_satisfaction(data)
            
            if prediction:
                last_id = insert_passenger(data, prediction)
                if last_id:
                    st.write(f"Registro {last_id} añadido a la base de datos con una predicción de satisfacción: **{prediction}**")
                    try:
                        if prediction == "Satisfied":
                            st.image(HAPPY_IMAGE_PATH, caption="Satisfied", use_column_width='always')
                        else:
                            st.image(SAD_IMAGE_PATH, caption="Neutral or Dissatisfied", use_column_width='always')
                    except Exception as e:
                        st.warning(f"La imagen no se pudo cargar. Verifica la ruta y el archivo. Error: {e}")
                else:
                    st.write("Ocurrió un error al insertar el registro en la base de datos.")
            else:
                st.write("Ocurrió un error al procesar su solicitud.")

        # Marcar que el formulario ha sido enviado
        st.session_state['form_submitted'] = True

    # Acción al presionar "Limpiar Formulario"
    if st.sidebar.button("Limpiar Formulario"):
        # Limpiar el estado de todos los campos del formulario
        st.session_state['gender'] = "Seleccionar"
        st.session_state['customer_type'] = "Seleccionar"
        st.session_state['age'] = 0
        st.session_state['type_of_travel'] = "Seleccionar"
        st.session_state['seat_class'] = "Seleccionar"
        st.session_state['flight_distance'] = 0
        st.session_state['inflight_wifi_service'] = 0
        st.session_state['departure_arrival_time_convenient'] = 0
        st.session_state['ease_of_online_booking'] = 0
        st.session_state['gate_location'] = 0
        st.session_state['food_and_drink'] = 0
        st.session_state['online_boarding'] = 0
        st.session_state['seat_comfort'] = 0
        st.session_state['inflight_entertainment'] = 0
        st.session_state['on_board_service'] = 0
        st.session_state['leg_room_service'] = 0
        st.session_state['baggage_handling'] = 0
        st.session_state['checkin_service'] = 0
        st.session_state['inflight_service'] = 0
        st.session_state['cleanliness'] = 0
        st.session_state['departure_delay_in_minutes'] = 0
        st.session_state['arrival_delay_in_minutes'] = 0
        st.session_state['form_submitted'] = False

        # Recargar la página para limpiar el formulario
        st.rerun()

    # Mostrar métricas de rendimiento del modelo en la barra lateral derecha
    with st.sidebar:
        st.header("Datos del Modelo")
        st.write(f"**Exactitud:** 0.98")
        st.write(f"**Recall:** 0.96")
        st.write(f"**F1 Score:** 0.97")
        st.write(f"**ROC AUC:** 1.00")

if __name__ == "__main__":
    main()
