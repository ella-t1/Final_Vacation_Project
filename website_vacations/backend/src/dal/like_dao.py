"""Data Access Object for Likes table."""

from typing import Iterable, Optional

from src.dal.base_dao import BaseDAO


class LikeDAO(BaseDAO):
    """DAO for managing likes in the database."""

    def list_all(self) -> Iterable[dict]:
        """Retrieve all likes from the database."""
        with self._cursor() as cur:
            cur.execute("SELECT user_id, vacation_id FROM likes ORDER BY user_id, vacation_id")
            return cur.fetchall()

    def get_by_user_and_vacation(self, user_id: int, vacation_id: int) -> Optional[dict]:
        """Retrieve a like by user_id and vacation_id."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT user_id, vacation_id FROM likes WHERE user_id = %s AND vacation_id = %s",
                (user_id, vacation_id)
            )
            return cur.fetchone()
    
    def get_by_user_id(self, user_id: int) -> Iterable[dict]:
        """Retrieve all likes for a specific user."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT user_id, vacation_id FROM likes WHERE user_id = %s",
                (user_id,)
            )
            return cur.fetchall()

    def get_by_id(self, composite_key: tuple[int, int]) -> Optional[dict]:
        """Retrieve a like by composite key (user_id, vacation_id)."""
        user_id, vacation_id = composite_key
        return self.get_by_user_and_vacation(user_id, vacation_id)

    def insert(self, data: dict) -> tuple[int, int]:
        """Insert a new like and return the composite key (user_id, vacation_id)."""
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO likes (user_id, vacation_id) VALUES (%s, %s) RETURNING user_id, vacation_id",
                (data["user_id"], data["vacation_id"])
            )
            result = cur.fetchone()
            return (result["user_id"], result["vacation_id"])

    def delete_by_user_and_vacation(self, user_id: int, vacation_id: int) -> int:
        """Delete a like by user_id and vacation_id. Returns number of rows affected."""
        with self._cursor() as cur:
            cur.execute(
                "DELETE FROM likes WHERE user_id = %s AND vacation_id = %s",
                (user_id, vacation_id)
            )
            return cur.rowcount

    def update_by_id(self, composite_key: tuple[int, int], data: dict) -> int:
        """Update is not applicable for likes table (composite key only)."""
        raise NotImplementedError("Likes table does not support updates")

    def delete_by_id(self, composite_key: tuple[int, int]) -> int:
        """Delete a like by composite key (user_id, vacation_id)."""
        user_id, vacation_id = composite_key
        return self.delete_by_user_and_vacation(user_id, vacation_id)
    
    def count_by_vacation(self, vacation_id: int) -> int:
        """Count total likes for a specific vacation."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM likes WHERE vacation_id = %s",
                (vacation_id,)
            )
            result = cur.fetchone()
            return result["count"] if result else 0
    
    def get_likes_count_by_vacation(self) -> dict[int, int]:
        """Get likes count for all vacations. Returns dict mapping vacation_id to count."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT vacation_id, COUNT(*) as count FROM likes GROUP BY vacation_id"
            )
            results = cur.fetchall()
            return {row["vacation_id"]: row["count"] for row in results}

