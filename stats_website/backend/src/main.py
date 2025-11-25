"""Main entry point for running the Flask application."""

import os
from src.api.app import create_app

if __name__ == "__main__":
    app = create_app()
    
    # Get port from environment or default to 5001
    port = int(os.getenv("FLASK_PORT", "5001"))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    app.run(host="0.0.0.0", port=port, debug=debug)

