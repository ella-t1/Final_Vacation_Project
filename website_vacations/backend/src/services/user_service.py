"""Business Logic Layer for User operations."""

import re
from typing import Optional

from src.dal.like_dao import LikeDAO
from src.dal.role_dao import RoleDAO
from src.dal.user_dao import UserDAO
from src.models.dtos import RoleName, UserDTO


class UserService:
    """Service for managing user-related business logic."""

    def __init__(self) -> None:
        """Initialize UserService with required DAOs."""
        self._user_dao = UserDAO()
        self._role_dao = RoleDAO()
        self._like_dao = LikeDAO()

    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _validate_password(self, password: str) -> bool:
        """Validate password (minimum 4 characters)."""
        return len(password) >= 4

    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        username: Optional[str] = None
    ) -> UserDTO:
        """
        Register a new user in the system.
        
        Validations:
        - All fields are mandatory (except username)
        - Email must be valid format
        - Password must be at least 4 characters
        - Email must not already exist in the system
        - Only regular users can be registered (Admin must be added manually)
        
        Args:
            first_name: User's first name
            last_name: User's last name
            email: User's email address
            password: User's password (min 4 chars)
            username: Optional username
            
        Returns:
            UserDTO: The newly created user
            
        Raises:
            ValueError: If validation fails
        """
        # Validate all mandatory fields
        if not first_name or not first_name.strip():
            raise ValueError("First name is mandatory")
        if not last_name or not last_name.strip():
            raise ValueError("Last name is mandatory")
        if not email or not email.strip():
            raise ValueError("Email is mandatory")
        if not password:
            raise ValueError("Password is mandatory")

        # Validate email format
        if not self._validate_email(email):
            raise ValueError("Invalid email format")

        # Validate password length
        if not self._validate_password(password):
            raise ValueError("Password must be at least 4 characters")

        # Check if email already exists
        if self._user_dao.email_exists(email):
            raise ValueError("Email already exists in the system")

        # Get User role ID (role_id = 2 for regular users)
        user_role = self._role_dao.get_by_name(RoleName.USER.value)
        if not user_role:
            raise ValueError("User role not found in database")

        # Insert new user
        user_data = {
            "first_name": first_name.strip(),
            "last_name": last_name.strip(),
            "email": email.strip().lower(),
            "password": password,
            "username": username.strip() if username else None,
            "role_id": user_role["id"],
        }

        user_id = self._user_dao.insert(user_data)

        # Return UserDTO (without password)
        return UserDTO(
            id=user_id,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            username=user_data["username"],
            role_id=user_data["role_id"],
        )

    def login(self, email: str, password: str) -> UserDTO:
        """
        Authenticate a user and return user information.
        
        Validations:
        - Email and password are mandatory
        - Email must be valid format
        - Password must be at least 4 characters
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            UserDTO: The authenticated user
            
        Raises:
            ValueError: If validation fails or credentials are invalid
        """
        # Validate mandatory fields
        if not email or not email.strip():
            raise ValueError("Email is mandatory")
        if not password:
            raise ValueError("Password is mandatory")

        # Validate email format
        if not self._validate_email(email):
            raise ValueError("Invalid email format")

        # Validate password length
        if not self._validate_password(password):
            raise ValueError("Password must be at least 4 characters")

        # Authenticate user
        user = self._user_dao.get_by_email_and_password(email.strip().lower(), password)
        if not user:
            raise ValueError("Invalid email or password")

        return UserDTO(
            id=user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            email=user["email"],
            username=user.get("username"),
            role_id=user["role_id"],
        )

    def like_vacation(self, user_id: int, vacation_id: int) -> None:
        """
        Add a like for a vacation by a user.
        
        Args:
            user_id: ID of the user
            vacation_id: ID of the vacation
            
        Raises:
            ValueError: If the like already exists or IDs are invalid
        """
        # Check if like already exists
        existing_like = self._like_dao.get_by_user_and_vacation(user_id, vacation_id)
        if existing_like:
            raise ValueError("User has already liked this vacation")

        # Insert new like
        like_data = {
            "user_id": user_id,
            "vacation_id": vacation_id,
        }
        self._like_dao.insert(like_data)

    def unlike_vacation(self, user_id: int, vacation_id: int) -> None:
        """
        Remove a like for a vacation by a user.
        
        Args:
            user_id: ID of the user
            vacation_id: ID of the vacation
            
        Raises:
            ValueError: If the like does not exist
        """
        # Check if like exists
        existing_like = self._like_dao.get_by_user_and_vacation(user_id, vacation_id)
        if not existing_like:
            raise ValueError("User has not liked this vacation")

        # Delete the like
        rows_affected = self._like_dao.delete_by_user_and_vacation(user_id, vacation_id)
        if rows_affected == 0:
            raise ValueError("Failed to unlike vacation")


