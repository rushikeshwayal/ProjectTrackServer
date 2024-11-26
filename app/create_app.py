def create_app():
    app = Flask(__name__)
    connection_string = os.getenv('connection_string')
    if not connection_string:
        raise RuntimeError("Environment variable 'connection_string' is not set")
    
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    
    db.init_app(app)
    register_blueprints(app)
    
    return app
