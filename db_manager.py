import sqlite3
from datetime import datetime

DB_PATH = 'dashboard.db'


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS DisplayState (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                production INTEGER NOT NULL,
                heats INTEGER NOT NULL,
                monthly_production INTEGER NOT NULL,
                safety_slogan TEXT NOT NULL,
                manpower_strength INTEGER NOT NULL,
                employee_month TEXT NOT NULL,
                image_path TEXT,
                image_expiry TEXT,
                last_updated TEXT NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS DisplayLog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                field TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT
            );
        ''')
        # Ensure a single row exists in DisplayState
        cursor.execute("SELECT COUNT(*) FROM DisplayState")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO DisplayState (
                    id, production, heats, monthly_production, safety_slogan,
                    manpower_strength, employee_month, image_path,
                    image_expiry, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (1, 0, 0, 0, 'Safety First!', 0, 'John Doe', None, None, datetime.now().isoformat()))

        conn.commit()


def get_display_state():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM DisplayState WHERE id = 1")
        row = cursor.fetchone()
        if row:
            return {
                'production': row[1],
                'heats': row[2],
                'monthly_production': row[3],
                'safety_slogan': row[4],
                'manpower_strength': row[5],
                'employee_month': row[6],
                'image_path': row[7],
                'image_expiry': row[8],
                'last_updated': row[9]
            }
        return None


def update_display_state(fields):
    current = get_display_state()
    changes = []
    for key in fields:
        old = current.get(key)
        new = fields[key]
        if str(old) != str(new):
            changes.append((datetime.now().isoformat(), key, str(old), str(new)))

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE DisplayState SET
                production = ?,
                heats = ?,
                monthly_production = ?,
                safety_slogan = ?,
                manpower_strength = ?,
                employee_month = ?,
                image_path = ?,
                image_expiry = ?,
                last_updated = ?
            WHERE id = 1
        """, (
            fields['production'],
            fields['heats'],
            fields['monthly_production'],
            fields['safety_slogan'],
            fields['manpower_strength'],
            fields['employee_month'],
            fields.get('image_path'),
            fields.get('image_expiry'),
            fields['last_updated']
        ))

        cursor.executemany("""
            INSERT INTO DisplayLog (timestamp, field, old_value, new_value)
            VALUES (?, ?, ?, ?)
        """, changes)

        conn.commit()
