from flask import Flask
from app.extensions import mongo, login_manager
from config import Config
from flask_cors import CORS

from flask_jwt_extended import JWTManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    CORS(app)
    
    jwt = JWTManager(app)

    # User loader for login management
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # Import routes
    from app.routes import init_app as setup_routes
    setup_routes(app)
    
    return app
