from models import create_tables
import os

os.makedirs('database', exist_ok=True)

create_tables()
print("✅ Database and tables created successfully.")
