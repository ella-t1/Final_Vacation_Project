"""Data Access Object for Roles table."""

from typing import Iterable, Optional

from src.dal.base_dao import BaseDAO


class RoleDAO(BaseDAO):
    """DAO for managing roles in the database."""

    def list_all(self) -> Iterable[dict]:
        """Retrieve all roles from the database."""
        with self._cursor() as cur:
            cur.execute("SELECT id, name FROM roles ORDER BY id")
            return cur.fetchall()

    def get_by_id(self, role_id: int) -> Optional[dict]:
        """Retrieve a role by its ID."""
        with self._cursor() as cur:
            cur.execute("SELECT id, name FROM roles WHERE id = %s", (role_id,))
            return cur.fetchone()

    def get_by_name(self, name: str) -> Optional[dict]:
        """Retrieve a role by its name."""
        with self._cursor() as cur:
            cur.execute("SELECT id, name FROM roles WHERE name = %s", (name,))
            return cur.fetchone()

    def insert(self, data: dict) -> int:
        """Insert a new role and return its ID."""
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO roles (name) VALUES (%s) RETURNING id",
                (data["name"],)
            )
            result = cur.fetchone()
            return result["id"]

    def update_by_id(self, role_id: int, data: dict) -> int:
        """Update a role by its ID. Returns number of rows affected."""
        with self._cursor() as cur:
            cur.execute(
                "UPDATE roles SET name = %s WHERE id = %s",
                (data["name"], role_id)
            )
            return cur.rowcount

    def delete_by_id(self, role_id: int) -> int:
        """Delete a role by its ID. Returns number of rows affected."""
        with self._cursor() as cur:
            cur.execute("DELETE FROM roles WHERE id = %s", (role_id,))
            return cur.rowcount

