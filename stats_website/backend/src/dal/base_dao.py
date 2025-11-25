"""Base Data Access Object with database connection management."""

from contextlib import contextmanager
from typing import Generator, Any, Iterable, Optional

import psycopg2
import psycopg2.extras

from src.config import get_connection_kwargs


class BaseDAO:
    """Base DAO class providing database connection management."""

    def __init__(self) -> None:
        """Initialize DAO with database connection parameters."""
        self._conn_kwargs = get_connection_kwargs()

    @contextmanager
    def _cursor(self) -> Generator[psycopg2.extensions.cursor, None, None]:
        """Context manager for database cursor."""
        conn = psycopg2.connect(**self._conn_kwargs)
        try:
            with conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    yield cur
        finally:
            conn.close()

    # Generic CRUD signatures (to be overridden in concrete DAOs)
    def list_all(self) -> Iterable[dict]:
        """List all entities."""
        raise NotImplementedError

    def get_by_id(self, entity_id: Any) -> Optional[dict]:
        """Get entity by ID."""
        raise NotImplementedError

    def insert(self, data: dict) -> Any:
        """Insert new entity."""
        raise NotImplementedError

    def update_by_id(self, entity_id: Any, data: dict) -> int:
        """Update entity by ID."""
        raise NotImplementedError

    def delete_by_id(self, entity_id: Any) -> int:
        """Delete entity by ID."""
        raise NotImplementedError

