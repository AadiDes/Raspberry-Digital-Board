import sqlite3
import os
from datetime import datetime
from config import DATABASE

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return dict-like rows
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Table: DisplayState
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DisplayState (
            id INTEGER PRIMARY KEY,
            production TEXT,
            num_heats TEXT,
            month_prod TEXT,
            slogan TEXT,
            manpower TEXT,
            employee_name TEXT,
            image_path TEXT,
            image_expiry TEXT,
            updated_at TEXT
        );
    """)

    # Table: DisplayLog
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DisplayLog (
            id INTEGER PRIMARY KEY,
            field TEXT,
            old_value TEXT,
            new_value TEXT,
            updated_by TEXT,
            updated_at TEXT
        );
    """)

    # Insert initial row into DisplayState if empty
    cursor.execute("SELECT COUNT(*) FROM DisplayState;")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO DisplayState (
                production, num_heats, month_prod, slogan,
                manpower, employee_name, image_path,
                image_expiry, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            "000", "00", "00000", "Safety First", "000",
            "Employee", "", "", datetime.utcnow().isoformat()
        ))

    conn.commit()
    conn.close()
