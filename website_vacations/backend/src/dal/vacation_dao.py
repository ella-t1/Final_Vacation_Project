"""Data Access Object for Vacations table."""

from datetime import date
from typing import Iterable, Optional

from src.dal.base_dao import BaseDAO


class VacationDAO(BaseDAO):
    """DAO for managing vacations in the database."""

    def list_all(self) -> Iterable[dict]:
        """Retrieve all vacations from the database, sorted by start_date ascending."""
        with self._cursor() as cur:
            cur.execute(
                """SELECT id, country_id, description, start_date, end_date, price, image_name
                   FROM vacations ORDER BY start_date ASC"""
            )
            return cur.fetchall()

    def get_by_id(self, vacation_id: int) -> Optional[dict]:
        """Retrieve a vacation by its ID."""
        with self._cursor() as cur:
            cur.execute(
                """SELECT id, country_id, description, start_date, end_date, price, image_name
                   FROM vacations WHERE id = %s""",
                (vacation_id,)
            )
            return cur.fetchone()

    def insert(self, data: dict) -> int:
        """Insert a new vacation and return its ID."""
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO vacations (country_id, description, start_date, end_date, price, image_name)
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                (
                    data["country_id"],
                    data["description"],
                    data["start_date"],
                    data["end_date"],
                    data["price"],
                    data.get("image_name"),
                )
            )
            result = cur.fetchone()
            return result["id"]

    def update_by_id(self, vacation_id: int, data: dict) -> int:
        """Update a vacation by its ID. Returns number of rows affected."""
        # Build dynamic UPDATE query based on provided fields
        updates = []
        values = []
        
        if "country_id" in data:
            updates.append("country_id = %s")
            values.append(data["country_id"])
        if "description" in data:
            updates.append("description = %s")
            values.append(data["description"])
        if "start_date" in data:
            updates.append("start_date = %s")
            values.append(data["start_date"])
        if "end_date" in data:
            updates.append("end_date = %s")
            values.append(data["end_date"])
        if "price" in data:
            updates.append("price = %s")
            values.append(data["price"])
        if "image_name" in data:
            updates.append("image_name = %s")
            values.append(data["image_name"])
        
        if not updates:
            return 0
        
        values.append(vacation_id)
        query = f"UPDATE vacations SET {', '.join(updates)} WHERE id = %s"
        
        with self._cursor() as cur:
            cur.execute(query, values)
            return cur.rowcount

    def delete_by_id(self, vacation_id: int) -> int:
        """Delete a vacation by its ID. Returns number of rows affected.
        Note: Likes are automatically deleted due to CASCADE constraint."""
        with self._cursor() as cur:
            cur.execute("DELETE FROM vacations WHERE id = %s", (vacation_id,))
            return cur.rowcount

