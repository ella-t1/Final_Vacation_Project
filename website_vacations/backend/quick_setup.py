"""Quick database setup script."""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "123456"
}

def create_databases():
    """Create vacations and test_db databases."""
    print("Connecting to PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        databases = ["vacations", "test_db"]
        
        for db_name in databases:
            print(f"Creating database '{db_name}'...")
            try:
                cur.execute(f'CREATE DATABASE "{db_name}"')
                print(f"  Database '{db_name}' created successfully!")
            except psycopg2.errors.DuplicateDatabase:
                print(f"  Database '{db_name}' already exists.")
        
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def initialize_schema(db_name):
    """Initialize schema for a database."""
    schema_path = Path(__file__).parent / "sql" / "schema.sql"
    
    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}")
        return False
    
    print(f"Initializing schema for '{db_name}'...")
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=db_name,
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cur = conn.cursor()
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cur.execute(schema_sql)
        conn.commit()
        cur.close()
        conn.close()
        print(f"  Schema initialized for '{db_name}'!")
        return True
    except Exception as e:
        print(f"  Error initializing schema: {e}")
        return False

def main():
    print("=" * 60)
    print("PostgreSQL Database Setup")
    print("=" * 60)
    print()
    
    # Create databases
    if not create_databases():
        print("\nFailed to create databases.")
        return
    
    print()
    
    # Initialize schemas
    databases = ["vacations", "test_db"]
    for db_name in databases:
        if not initialize_schema(db_name):
            print(f"\nFailed to initialize schema for {db_name}.")
            return
        print()
    
    print("=" * 60)
    print("Database setup completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()

