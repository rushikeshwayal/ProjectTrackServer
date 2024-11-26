from flask import Flask
from app.extensions import db
from app.routes import register_blueprints
from app.config import Config
from dotenv import load_dotenv
import os

load_dotenv()  # Ensure this is called early in the app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    register_blueprints(app)

    return app
