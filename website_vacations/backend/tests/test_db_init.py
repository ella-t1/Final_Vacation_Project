"""Test database initialization helper."""

import os
import psycopg2
from pathlib import Path


def init_test_db() -> None:
    """
    Initialize the test database by executing the schema SQL script.
    This should be called at the beginning of each test run.
    """
    # Read the schema SQL file
    schema_path = Path(__file__).parent.parent / "sql" / "schema.sql"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Connect to test_db
    conn_kwargs = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "test_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }

    conn = psycopg2.connect(**conn_kwargs)
    try:
        with conn.cursor() as cur:
            # Execute the schema SQL
            cur.execute(schema_sql)
        conn.commit()
    finally:
        conn.close()

