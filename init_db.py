from models import create_tables
import os

if not os.path.exists('database'):
    os.makedirs('database')

create_tables()
print("✅ Database and tables created successfully.")
