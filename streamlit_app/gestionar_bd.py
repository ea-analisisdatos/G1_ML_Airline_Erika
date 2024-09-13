import sqlite3
import os

# Función para conectarse a la base de datos usando una ruta absoluta
def connect_db():
    try:
        # Usa la ruta absoluta de la base de datos
        db_path = os.path.abspath('../data/database/airline_satisfaction.db')
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"El archivo de base de datos no existe: {db_path}")
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para eliminar una tabla en la base de datos
def eliminar_tabla(nombre_tabla):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS {nombre_tabla}")
            conn.commit()
            conn.close()
            print(f"Tabla '{nombre_tabla}' eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la tabla {nombre_tabla}: {e}")
    else:
        print(f"No se pudo establecer conexión con la base de datos.")

# Función para listar todas las tablas en la base de datos
def listar_tablas():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = cursor.fetchall()
            conn.close()
            return tablas
        except Exception as e:
            print(f"Error al listar tablas: {e}")
            return []
    else:
        return []

# Eliminar una tabla específica
nombre_tabla = "modelos_entrenados"  # Cambia el nombre de la tabla si es necesario
eliminar_tabla(nombre_tabla)

# Verificar todas las tablas existentes en la base de datos
tablas = listar_tablas()
if tablas is not None:
    print("Tablas en la base de datos:")
    for tabla in tablas:
        print(tabla[0])
else:
    print("No se pudieron listar las tablas.")
