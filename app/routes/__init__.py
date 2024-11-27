from flask import Flask
from app.extensions import db
from app.config import Config
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    # Import models to register them with SQLAlchemy
    from app.models import Admin

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

def register_blueprints(app):
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api')  # Example: prefix routes with /api


    return app
