# streamlit_app/initialize_db.py
import sqlite3
from pathlib import Path
from config import DB_NAME

def create_database():
    try:
        # Convertir DB_NAME a una ruta de pathlib
        db_path = Path(DB_NAME)
        
        # Verificar si el directorio padre existe, si no, crear
        if not db_path.parent.exists():
            db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Conectar o crear la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Crear la tabla de pasajeros si no existe
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pasajeros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT,
            customer_type TEXT,
            age INTEGER,
            type_of_travel TEXT,
            seat_class TEXT,
            flight_distance INTEGER,
            inflight_wifi_service INTEGER,
            departure_arrival_time_convenient INTEGER,
            ease_of_online_booking INTEGER,
            gate_location INTEGER,
            food_and_drink INTEGER,
            online_boarding INTEGER,
            seat_comfort INTEGER,
            inflight_entertainment INTEGER,
            on_board_service INTEGER,
            leg_room_service INTEGER,
            baggage_handling INTEGER,
            checkin_service INTEGER,
            inflight_service INTEGER,
            cleanliness INTEGER,
            departure_delay_in_minutes INTEGER,
            arrival_delay_in_minutes INTEGER,
            satisfaction TEXT,
            satisfaction_predicted TEXT
        )
        ''')

        conn.commit()
        conn.close()
        print("Base de datos creada exitosamente.")

    except sqlite3.Error as e:
        print(f"Error al conectar o crear la base de datos: {e}")

if __name__ == "__main__":
    create_database()
