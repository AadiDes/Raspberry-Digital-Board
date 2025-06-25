from flask import Flask
from app.routes import main
from app.db_utils import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    init_db()  # <--- Initialize tables if not present

    app.register_blueprint(main)
    return app

