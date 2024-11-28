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
    from app.models import Admin, Investigator, Agency, SubInvestigator  # Added SubInvestigator and Agency models

    # Register blueprints
    register_blueprints(app)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

def register_blueprints(app):
    from app.routes.admin import admin_bp
    from app.routes.investigator import investigator_bp
    from app.routes.agency import agency_bp
    from app.routes.SubInvestigator import sub_investigator_bp  # Register SubInvestigator blueprint
    from app.routes.SubAgency import sub_agency_bp
    from app.routes.ProjectFund import project_fund_bp  # Import the project_fund blueprint
    from app.routes.ProjectStatus import project_status_bp 
    from app.routes.Project import project_bp
    from app.routes.ProjectCoordinator import projectcoordinator_bp



    # Register all blueprints with a common API prefix
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(investigator_bp, url_prefix='/api')
    app.register_blueprint(agency_bp, url_prefix='/api')
    app.register_blueprint(sub_investigator_bp, url_prefix='/api')
    app.register_blueprint(sub_agency_bp,url_prefix='/api')
    app.register_blueprint(project_fund_bp, url_prefix='/api')  
    app.register_blueprint(project_status_bp, url_prefix='/api')
    app.register_blueprint(project_bp, url_prefix='/api')
    app.register_blueprint(projectcoordinator_bp, url_prefix='/api')


    


