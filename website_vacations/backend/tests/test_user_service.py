"""Comprehensive tests for UserService."""

import pytest

from src.services.user_service import UserService
from tests.test_db_init import init_test_db


@pytest.fixture(autouse=True)
def setup_test_db():
    """Initialize test database before each test."""
    init_test_db()


class TestUserService:
    """Test suite for UserService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = UserService()

    # ========== Register User Tests ==========

    def test_register_user_success(self):
        """Positive test: Register a new user successfully."""
        user = self.service.register_user(
            "Jane", "Smith", "jane@example.com", "password123", "janesmith"
        )
        assert user.id > 0
        assert user.first_name == "Jane"
        assert user.last_name == "Smith"
        assert user.email == "jane@example.com"
        assert user.username == "janesmith"
        assert user.role_id == 2  # User role

    def test_register_user_minimal_fields(self):
        """Positive test: Register user with minimal required fields."""
        user = self.service.register_user(
            "Bob", "Johnson", "bob@example.com", "pass1234"
        )
        assert user.id > 0
        assert user.email == "bob@example.com"
        assert user.username is None

    def test_register_user_empty_first_name(self):
        """Negative test: Empty first name."""
        with pytest.raises(ValueError, match="First name is mandatory"):
            self.service.register_user("", "Doe", "test@example.com", "pass1234")

    def test_register_user_empty_last_name(self):
        """Negative test: Empty last name."""
        with pytest.raises(ValueError, match="Last name is mandatory"):
            self.service.register_user("John", "", "test@example.com", "pass1234")

    def test_register_user_empty_email(self):
        """Negative test: Empty email."""
        with pytest.raises(ValueError, match="Email is mandatory"):
            self.service.register_user("John", "Doe", "", "pass1234")

    def test_register_user_empty_password(self):
        """Negative test: Empty password."""
        with pytest.raises(ValueError, match="Password is mandatory"):
            self.service.register_user("John", "Doe", "test@example.com", "")

    def test_register_user_invalid_email_format(self):
        """Negative test: Invalid email format."""
        with pytest.raises(ValueError, match="Invalid email format"):
            self.service.register_user("John", "Doe", "invalid-email", "pass1234")

    def test_register_user_short_password(self):
        """Negative test: Password too short."""
        with pytest.raises(ValueError, match="Password must be at least 4 characters"):
            self.service.register_user("John", "Doe", "test@example.com", "abc")

    def test_register_user_duplicate_email(self):
        """Negative test: Email already exists."""
        # Register first user
        self.service.register_user("First", "User", "duplicate@example.com", "pass1234")
        # Try to register with same email
        with pytest.raises(ValueError, match="Email already exists"):
            self.service.register_user("Second", "User", "duplicate@example.com", "pass1234")

    # ========== Login Tests ==========

    def test_login_success(self):
        """Positive test: Login with valid credentials."""
        # First register a user
        registered_user = self.service.register_user(
            "Login", "Test", "login@example.com", "mypassword123"
        )
        # Then login
        logged_in_user = self.service.login("login@example.com", "mypassword123")
        assert logged_in_user.id == registered_user.id
        assert logged_in_user.email == "login@example.com"

    def test_login_with_existing_user(self):
        """Positive test: Login with existing seeded user."""
        # Use seeded user from schema.sql
        user = self.service.login("john@example.com", "user1234")
        assert user.email == "john@example.com"
        assert user.role_id == 2  # User role

    def test_login_empty_email(self):
        """Negative test: Empty email."""
        with pytest.raises(ValueError, match="Email is mandatory"):
            self.service.login("", "password123")

    def test_login_empty_password(self):
        """Negative test: Empty password."""
        with pytest.raises(ValueError, match="Password is mandatory"):
            self.service.login("test@example.com", "")

    def test_login_invalid_email_format(self):
        """Negative test: Invalid email format."""
        with pytest.raises(ValueError, match="Invalid email format"):
            self.service.login("invalid-email", "password123")

    def test_login_short_password(self):
        """Negative test: Password too short."""
        with pytest.raises(ValueError, match="Password must be at least 4 characters"):
            self.service.login("test@example.com", "abc")

    def test_login_wrong_email(self):
        """Negative test: Wrong email."""
        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("nonexistent@example.com", "password123")

    def test_login_wrong_password(self):
        """Negative test: Wrong password."""
        # Register a user first
        self.service.register_user("Test", "User", "wrongpass@example.com", "correctpass")
        # Try to login with wrong password
        with pytest.raises(ValueError, match="Invalid email or password"):
            self.service.login("wrongpass@example.com", "wrongpassword")

    # ========== Like Vacation Tests ==========

    def test_like_vacation_success(self):
        """Positive test: Like a vacation successfully."""
        # Register a user
        user = self.service.register_user("Like", "User", "like@example.com", "pass1234")
        # Like vacation ID 1 (from seed data)
        self.service.like_vacation(user.id, 1)
        # Should not raise exception

    def test_like_vacation_duplicate(self):
        """Negative test: Like same vacation twice."""
        user = self.service.register_user("Duplicate", "User", "duplicate@example.com", "pass1234")
        self.service.like_vacation(user.id, 1)
        # Try to like again
        with pytest.raises(ValueError, match="already liked"):
            self.service.like_vacation(user.id, 1)

    # ========== Unlike Vacation Tests ==========

    def test_unlike_vacation_success(self):
        """Positive test: Unlike a vacation successfully."""
        user = self.service.register_user("Unlike", "User", "unlike@example.com", "pass1234")
        # First like
        self.service.like_vacation(user.id, 1)
        # Then unlike
        self.service.unlike_vacation(user.id, 1)
        # Should not raise exception

    def test_unlike_vacation_not_liked(self):
        """Negative test: Unlike a vacation that wasn't liked."""
        user = self.service.register_user("NoLike", "User", "nolike@example.com", "pass1234")
        with pytest.raises(ValueError, match="has not liked"):
            self.service.unlike_vacation(user.id, 1)
