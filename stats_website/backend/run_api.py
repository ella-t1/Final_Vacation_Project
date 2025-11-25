"""Run the Flask API server for statistics website."""

from dotenv import load_dotenv
from src.api.app import create_app

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    print("Starting Statistics API server on http://localhost:5001")
    print("API endpoints available at http://localhost:5001/")
    print("\nEndpoints:")
    print("  GET  /health")
    print("  POST /login")
    print("  POST /logout")
    print("  GET  /vacations/stats (requires auth)")
    print("  GET  /users/total (requires auth)")
    print("  GET  /likes/total (requires auth)")
    print("  GET  /likes/distribution (requires auth)")
    app.run(debug=True, host="0.0.0.0", port=5001)

