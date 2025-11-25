"""Flask application factory and configuration."""

from flask import Flask
from flask_cors import CORS

from src.api.routes import register_routes


def create_app() -> Flask:
    """Create and configure Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Configure secret key for sessions
    app.config["SECRET_KEY"] = "your-secret-key-change-in-production"
    
    # Enable CORS for frontend
    CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:3001"])
    
    # Register routes
    register_routes(app)
    
    return app

