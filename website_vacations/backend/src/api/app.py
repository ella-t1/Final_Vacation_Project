"""Flask application for Vacations API."""

from flask import Flask
from flask_cors import CORS

from src.api.routes import register_routes


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app, origins=["http://localhost:5173", "http://localhost:3000"], supports_credentials=True)
    
    # Register routes
    register_routes(app)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)


