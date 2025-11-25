"""Data Access Object for Countries table."""

from typing import Iterable, Optional

from src.dal.base_dao import BaseDAO


class CountryDAO(BaseDAO):
    """DAO for managing countries in the database."""

    def list_all(self) -> Iterable[dict]:
        """Retrieve all countries from the database."""
        with self._cursor() as cur:
            cur.execute("SELECT id, name FROM countries ORDER BY name")
            return cur.fetchall()

    def get_by_id(self, country_id: int) -> Optional[dict]:
        """Retrieve a country by its ID."""
        with self._cursor() as cur:
            cur.execute("SELECT id, name FROM countries WHERE id = %s", (country_id,))
            return cur.fetchone()

    def insert(self, data: dict) -> int:
        """Insert a new country and return its ID."""
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO countries (name) VALUES (%s) RETURNING id",
                (data["name"],)
            )
            result = cur.fetchone()
            return result["id"]

    def update_by_id(self, country_id: int, data: dict) -> int:
        """Update a country by its ID. Returns number of rows affected."""
        with self._cursor() as cur:
            cur.execute(
                "UPDATE countries SET name = %s WHERE id = %s",
                (data["name"], country_id)
            )
            return cur.rowcount

    def delete_by_id(self, country_id: int) -> int:
        """Delete a country by its ID. Returns number of rows affected."""
        with self._cursor() as cur:
            cur.execute("DELETE FROM countries WHERE id = %s", (country_id,))
            return cur.rowcount

