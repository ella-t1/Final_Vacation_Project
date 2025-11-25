"""Authentication service for statistics website."""

from typing import Optional
from flask import session

from src.dal.user_dao import UserDAO
from src.dal.role_dao import RoleDAO


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self) -> None:
        """Initialize authentication service with DAOs."""
        self.user_dao = UserDAO()
        self.role_dao = RoleDAO()

    def login(self, username: str, password: str) -> dict:
        """Login user with username and password.
        
        Args:
            username: Username or email of the user
            password: User password
            
        Returns:
            dict: User information if login successful
            
        Raises:
            ValueError: If credentials are invalid or user is not admin
        """
        # Try username first, then email
        user = self.user_dao.get_by_username_and_password(username, password)
        if not user:
            user = self.user_dao.get_by_email_and_password(username, password)
        
        if not user:
            raise ValueError("Invalid username or password")
        
        # Check if user is admin
        role = self.role_dao.get_by_id(user["role_id"])
        if not role or role["name"] != "Admin":
            raise ValueError("Admin access required")
        
        # Store user info in session
        session["user_id"] = user["id"]
        session["username"] = user.get("username") or user["email"]
        session["is_admin"] = True
        
        return {
            "id": user["id"],
            "firstName": user["first_name"],
            "lastName": user["last_name"],
            "email": user["email"],
            "username": user.get("username"),
            "roleId": user["role_id"],
        }

    def logout(self) -> None:
        """Logout current user by clearing session."""
        session.clear()

    def is_authenticated(self) -> bool:
        """Check if user is authenticated.
        
        Returns:
            bool: True if user is authenticated and is admin
        """
        return session.get("is_admin", False)

    def get_current_user_id(self) -> Optional[int]:
        """Get current authenticated user ID.
        
        Returns:
            Optional[int]: User ID if authenticated, None otherwise
        """
        if self.is_authenticated():
            return session.get("user_id")
        return None

    def is_admin(self, user_id: int) -> bool:
        """Check if a user is an admin.
        
        Args:
            user_id: User ID to check
            
        Returns:
            bool: True if user is admin
        """
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return False
        
        role = self.role_dao.get_by_id(user["role_id"])
        return role is not None and role["name"] == "Admin"

