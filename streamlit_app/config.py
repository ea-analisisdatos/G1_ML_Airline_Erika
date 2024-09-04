# streamlit_app/config.py
#DB_NAME = "../data/database/airline_satisfaction.db"

# streamlit_app/config.py
from pathlib import Path

# Definir la ruta de la base de datos usando pathlib
DB_NAME = Path(__file__).resolve().parent.parent / 'data' / 'database' / 'airline_satisfaction.db'
