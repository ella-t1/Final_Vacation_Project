"""API routes for Vacations application."""

from datetime import datetime
from flask import Flask, jsonify, request
from typing import Dict, Any

from src.dal.country_dao import CountryDAO
from src.services.user_service import UserService
from src.services.vacation_service import VacationService
from src.models.dtos import RoleName


def register_routes(app: Flask) -> None:
    """Register all API routes."""
    
    user_service = UserService()
    vacation_service = VacationService()
    country_dao = CountryDAO()
    
    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({"status": "ok"}), 200
    
    # User endpoints
    @app.route("/api/users/register", methods=["POST"])
    def register():
        """Register a new user."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            user = user_service.register_user(
                first_name=data.get("firstName", ""),
                last_name=data.get("lastName", ""),
                email=data.get("email", ""),
                password=data.get("password", ""),
            )
            
            return jsonify({
                "id": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "roleId": user.role_id,
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/api/users/login", methods=["POST"])
    def login():
        """Login user."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            user = user_service.login(
                email=data.get("email", ""),
                password=data.get("password", ""),
            )
            
            # Get role name to determine if admin
            from src.dal.role_dao import RoleDAO
            role_dao = RoleDAO()
            role = role_dao.get_by_id(user.role_id)
            is_admin = role and role["name"] == "Admin"
            
            return jsonify({
                "id": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "email": user.email,
                "roleId": user.role_id,
                "isAdmin": is_admin,
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/api/users/<int:user_id>/likes/<int:vacation_id>", methods=["POST"])
    def like_vacation(user_id: int, vacation_id: int):
        """Add a like to a vacation."""
        try:
            user_service.like_vacation(user_id, vacation_id)
            return jsonify({"message": "Vacation liked successfully"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/api/users/<int:user_id>/likes/<int:vacation_id>", methods=["DELETE"])
    def unlike_vacation(user_id: int, vacation_id: int):
        """Remove a like from a vacation."""
        try:
            user_service.unlike_vacation(user_id, vacation_id)
            return jsonify({"message": "Vacation unliked successfully"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    # Vacation endpoints
    @app.route("/api/vacations", methods=["GET"])
    def list_vacations():
        """Get all vacations sorted by start date."""
        try:
            vacations = vacation_service.list_vacations()
            vacations_list = []
            for v in vacations:
                vacations_list.append({
                    "id": v.id,
                    "countryId": v.country_id,
                    "description": v.description,
                    "startDate": v.start_date.isoformat() if v.start_date else None,
                    "endDate": v.end_date.isoformat() if v.end_date else None,
                    "price": v.price,
                    "imageName": v.image_name,
                })
            return jsonify(vacations_list), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/api/vacations/<int:vacation_id>", methods=["GET"])
    def get_vacation(vacation_id: int):
        """Get a single vacation by ID."""
        try:
            from src.dal.vacation_dao import VacationDAO
            vacation_dao = VacationDAO()
            vacation = vacation_dao.get_by_id(vacation_id)
            if not vacation:
                return jsonify({"error": "Vacation not found"}), 404
            
            return jsonify({
                "id": vacation["id"],
                "countryId": vacation["country_id"],
                "description": vacation["description"],
                "startDate": vacation["start_date"].isoformat() if vacation["start_date"] else None,
                "endDate": vacation["end_date"].isoformat() if vacation["end_date"] else None,
                "price": float(vacation["price"]),
                "imageName": vacation.get("image_name"),
            }), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/api/vacations", methods=["POST"])
    def create_vacation():
        """Create a new vacation."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Parse dates
            start_date = datetime.fromisoformat(data.get("startDate", "")).date()
            end_date = datetime.fromisoformat(data.get("endDate", "")).date()
            
            vacation = vacation_service.add_vacation(
                country_id=int(data.get("countryId", 0)),
                description=data.get("description", ""),
                start_date=start_date,
                end_date=end_date,
                price=float(data.get("price", 0)),
                image_name=data.get("imageName"),
            )
            
            return jsonify({
                "id": vacation.id,
                "countryId": vacation.country_id,
                "description": vacation.description,
                "startDate": vacation.start_date.isoformat(),
                "endDate": vacation.end_date.isoformat(),
                "price": vacation.price,
                "imageName": vacation.image_name,
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/api/vacations/<int:vacation_id>", methods=["PUT"])
    def update_vacation(vacation_id: int):
        """Update an existing vacation."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            
            # Parse dates if provided
            start_date = None
            end_date = None
            if data.get("startDate"):
                start_date = datetime.fromisoformat(data.get("startDate")).date()
            if data.get("endDate"):
                end_date = datetime.fromisoformat(data.get("endDate")).date()
            
            vacation = vacation_service.update_vacation(
                vacation_id=vacation_id,
                country_id=int(data["countryId"]) if data.get("countryId") is not None else None,
                description=data.get("description"),
                start_date=start_date,
                end_date=end_date,
                price=float(data["price"]) if data.get("price") is not None else None,
                image_name=data.get("imageName"),
            )
            
            return jsonify({
                "id": vacation.id,
                "countryId": vacation.country_id,
                "description": vacation.description,
                "startDate": vacation.start_date.isoformat(),
                "endDate": vacation.end_date.isoformat(),
                "price": vacation.price,
                "imageName": vacation.image_name,
            }), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    @app.route("/api/vacations/<int:vacation_id>", methods=["DELETE"])
    def delete_vacation(vacation_id: int):
        """Delete a vacation."""
        try:
            vacation_service.delete_vacation(vacation_id)
            return jsonify({"message": "Vacation deleted successfully"}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    # Country endpoints
    @app.route("/api/countries", methods=["GET"])
    def list_countries():
        """Get all countries."""
        try:
            countries = country_dao.list_all()
            countries_list = [{"id": c["id"], "name": c["name"]} for c in countries]
            return jsonify(countries_list), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
    # Likes endpoint - get likes for a user
    @app.route("/api/users/<int:user_id>/likes", methods=["GET"])
    def get_user_likes(user_id: int):
        """Get all vacations liked by a user."""
        try:
            from src.dal.like_dao import LikeDAO
            like_dao = LikeDAO()
            likes = like_dao.get_by_user_id(user_id)
            vacation_ids = [like["vacation_id"] for like in likes]
            return jsonify({"likedVacationIds": vacation_ids}), 200
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

