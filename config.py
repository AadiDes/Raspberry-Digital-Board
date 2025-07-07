from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.environ.get('SECRET_KEY')

# Path to your SQLite database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'database', 'factory.db')
