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
    from app.models import Admin, Investigator, Agency, ProjectFund

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Register blueprints
    register_blueprints(app)

    return app

def register_blueprints(app):
    from app.routes.admin import admin_bp
    from app.routes.investigator import investigator_bp
    from app.routes.agency import agency_bp
    from app.routes.ProjectFund import project_fund_bp  # Import the new blueprint

    app.register_blueprint(admin_bp, url_prefix='/api')  # Example: prefix routes with /api
    app.register_blueprint(investigator_bp, url_prefix='/api')  # Example: prefix routes with /api
    app.register_blueprint(agency_bp, url_prefix='/api')  # Example: prefix routes with /api
    app.register_blueprint(project_fund_bp, url_prefix='/api')  # Register Project Fund blueprint

    return app
