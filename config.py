import os

# Path to your SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'factory.db')

# Secret key for forms (you can generate a better one later)
SECRET_KEY = 'display_secret_key'
