import sqlite3
import os

db_path = os.path.join("database", "factory_dashboard.db")

if not os.path.exists(db_path):
    print("❌ Database file does not exist.")
    exit()

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Drop only the DisplayLog table
cur.execute("DROP TABLE IF EXISTS DisplayLog;")
conn.commit()
conn.close()

print("✅ Dropped DisplayLog table successfully.")
