"""Flask application for Vacations API."""

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from src.api.routes import register_routes


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    
    # Enable CORS for frontend
    CORS(app, origins=["http://localhost:5173" , "http://localhost:3000", "http://localhost:3001", "http://localhost:5174"], supports_credentials=True)
    
    # Create images directory if it doesn't exist
    images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images")
    os.makedirs(images_dir, exist_ok=True)
    
    # Serve static images
    @app.route("/images/<filename>")
    def serve_image(filename):
        """Serve vacation images."""
        return send_from_directory(images_dir, filename)
    
    # Register routes
    register_routes(app)
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)


