"""Run the Flask API server."""

from dotenv import load_dotenv
from src.api.app import create_app

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    print("Starting Vacations API server on http://localhost:5000")
    print("API endpoints available at http://localhost:5000/api/")
    app.run(debug=True, host="0.0.0.0", port=5000)


