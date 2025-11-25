"""Database configuration for statistics website backend."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DbConfig:
    """Database configuration dataclass."""
    host: str
    port: int
    name: str
    user: str
    password: str

    @staticmethod
    def from_env() -> "DbConfig":
        """Create DbConfig from environment variables."""
        return DbConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "vacations"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
        )


def get_connection_kwargs() -> dict:
    """Get database connection keyword arguments."""
    cfg = DbConfig.from_env()
    return {
        "host": cfg.host,
        "port": cfg.port,
        "dbname": cfg.name,
        "user": cfg.user,
        "password": cfg.password,
    }

