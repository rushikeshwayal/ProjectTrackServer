from flask import Flask
from app.extensions import db
from app.config import Config
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"])
    app.config.from_object(Config)

    db.init_app(app)

    from app.models import Admin

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

        # register blueprints for routes
         # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
