"""API routes for Statistics website."""

from functools import wraps
from flask import Flask, jsonify, request, session

from src.services.auth_service import AuthService
from src.services.statistics_service import StatisticsService


def admin_required(f):
    """Decorator to require admin authentication for routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_service = AuthService()
        if not auth_service.is_authenticated():
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated_function


def register_routes(app: Flask) -> None:
    """Register all API routes."""
    
    auth_service = AuthService()
    statistics_service = StatisticsService()
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "ok"}), 200
    
    @app.route("/login", methods=["POST"])
    def login():
        """Login endpoint - Admin only."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            username = data.get("username", "") or data.get("email", "")
            password = data.get("password", "")
            
            if not username or not password:
                return jsonify({"error": "Username and password are required"}), 400
            
            user = auth_service.login(username, password)
            return jsonify(user), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 403
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/logout", methods=["POST"])
    @admin_required
    def logout():
        """Logout endpoint."""
        try:
            auth_service.logout()
            return jsonify({"message": "Logged out successfully"}), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/vacations/stats", methods=["GET"])
    @admin_required
    def get_vacation_stats():
        """Get vacation statistics."""
        try:
            stats = statistics_service.get_vacation_stats()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/users/total", methods=["GET"])
    @admin_required
    def get_total_users():
        """Get total number of users."""
        try:
            stats = statistics_service.get_total_users()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/likes/total", methods=["GET"])
    @admin_required
    def get_total_likes():
        """Get total number of likes."""
        try:
            stats = statistics_service.get_total_likes()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/likes/distribution", methods=["GET"])
    @admin_required
    def get_likes_distribution():
        """Get likes distribution by destination."""
        try:
            distribution = statistics_service.get_likes_distribution()
            return jsonify(distribution), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

