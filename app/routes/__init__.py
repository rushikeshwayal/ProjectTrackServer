from flask import Flask
from app.extensions import db
from app.config import Config
from dotenv import load_dotenv
import os
from flask_cors import CORS
import base64
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"])
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
    from app.routes.message import message_bp
    from app.routes.form import upload_bp
    from app.routes.projectReport import project_Report_bp
    from app.routes.Allforms import file_bp
    from app.routes.FundUtilization import fund_utilization_bp  # Register the fund_utilization blueprint





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
    app.register_blueprint(message_bp, url_prefix='/api')
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(project_Report_bp, url_prefix='/api')
    app.register_blueprint(file_bp, url_prefix='/api')
    app.register_blueprint(fund_utilization_bp, url_prefix='/api')  # Register the fund_utilization blueprint
    



    


