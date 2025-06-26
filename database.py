import sqlite3
from datetime import datetime

DB_PATH = 'dashboard.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
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
        c.execute('''
            CREATE TABLE IF NOT EXISTS DisplayLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                updated_at DATETIME,
                changes TEXT
            )
        ''')
        # Ensure one default row exists in DisplayState
        c.execute("SELECT COUNT(*) FROM DisplayState")
        if c.fetchone()[0] == 0:
            c.execute('''
                INSERT INTO DisplayState 
                (production, heats, monthly_production, safety_slogan, manpower_strength, employee_month, image_path, image_expiry, last_updated)
                VALUES (0, 0, 0, 'Safety First!', 0, 'John Doe', NULL, NULL, ?)
            ''', (datetime.now(),))
        conn.commit()
