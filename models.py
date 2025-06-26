import sqlite3
from datetime import datetime

DB_PATH = 'database/factory_dashboard.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # DisplayState: stores current display data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DisplayState (
            id INTEGER PRIMARY KEY,
            production INTEGER,
            heats INTEGER,
            monthly_production INTEGER,
            safety_slogan TEXT,
            manpower_strength INTEGER,
            employee_month TEXT,
            image_path TEXT,
            image_expiry DATETIME,
            last_updated DATETIME
        )
    ''')

    # DisplayLog: historical updates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DisplayLog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            production INTEGER,
            heats INTEGER,
            monthly_production INTEGER,
            safety_slogan TEXT,
            manpower_strength INTEGER,
            employee_month TEXT
        )
    ''')

    conn.commit()
    conn.close()
