"""Data Access Object for Users table."""

from typing import Iterable, Optional

from src.dal.base_dao import BaseDAO


class UserDAO(BaseDAO):
    """DAO for managing users in the database."""

    def list_all(self) -> Iterable[dict]:
        """Retrieve all users from the database."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, email, username, role_id FROM users ORDER BY id"
            )
            return cur.fetchall()

    def get_by_id(self, user_id: int) -> Optional[dict]:
        """Retrieve a user by its ID."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, email, username, role_id FROM users WHERE id = %s",
                (user_id,)
            )
            return cur.fetchone()

    def get_by_email(self, email: str) -> Optional[dict]:
        """Retrieve a user by email (includes password for authentication)."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, email, password, username, role_id FROM users WHERE email = %s",
                (email,)
            )
            return cur.fetchone()

    def get_by_email_and_password(self, email: str, password: str) -> Optional[dict]:
        """Retrieve a user by email and password (for login)."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT id, first_name, last_name, email, username, role_id FROM users WHERE email = %s AND password = %s",
                (email, password)
            )
            return cur.fetchone()

    def email_exists(self, email: str) -> bool:
        """Check if an email already exists in the database."""
        with self._cursor() as cur:
            cur.execute("SELECT COUNT(*) as count FROM users WHERE email = %s", (email,))
            result = cur.fetchone()
            return result["count"] > 0

    def insert(self, data: dict) -> int:
        """Insert a new user and return its ID."""
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO users (first_name, last_name, email, password, username, role_id)
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                (
                    data["first_name"],
                    data["last_name"],
                    data["email"],
                    data["password"],
                    data.get("username"),
                    data["role_id"],
                )
            )
            result = cur.fetchone()
            return result["id"]

    def update_by_id(self, user_id: int, data: dict) -> int:
        """Update a user by its ID. Returns number of rows affected."""
        with self._cursor() as cur:
            cur.execute(
                """UPDATE users SET first_name = %s, last_name = %s, email = %s,
                   password = %s, username = %s, role_id = %s WHERE id = %s""",
                (
                    data["first_name"],
                    data["last_name"],
                    data["email"],
                    data.get("password"),
                    data.get("username"),
                    data.get("role_id"),
                    user_id,
                )
            )
            return cur.rowcount

    def delete_by_id(self, user_id: int) -> int:
        """Delete a user by its ID. Returns number of rows affected."""
        with self._cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
            return cur.rowcount

