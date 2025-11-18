"""Database setup script for Vacations project (Non-interactive version).

Usage:
    # Set environment variables first:
    $env:DB_PASSWORD="your_password"
    py setup_database.py

    # Or pass password directly:
    py setup_database.py your_password
"""

import os
import sys
from pathlib import Path

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
except ImportError:
    print("ERROR: psycopg2 is not installed. Please run:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def get_db_config(password=None):
    """Get database configuration from environment or command line."""
    print("=" * 60)
    print("PostgreSQL Database Setup")
    print("=" * 60)
    print()
    
    # Try to get from environment first
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    admin_user = os.getenv("DB_ADMIN_USER", "postgres")
    
    print(f"Using PostgreSQL server: {host}:{port}")
    print(f"Admin user: {admin_user}")
    print()
    
    # Get password from command line argument or environment
    if password:
        db_password = password
    else:
        db_password = os.getenv("DB_PASSWORD")
    
    if not db_password:
        print("ERROR: PostgreSQL password not provided!")
        print("\nPlease provide the password in one of these ways:")
        print("1. Set environment variable: $env:DB_PASSWORD='your_password'")
        print("2. Pass as argument: py setup_database.py your_password")
        print("\nThis is the password you set when installing PostgreSQL.")
        sys.exit(1)
    
    return {
        "host": host,
        "port": port,
        "user": admin_user,
        "password": db_password
    }


def test_connection(config):
    """Test connection to PostgreSQL server."""
    print("Testing connection to PostgreSQL server...")
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname="postgres",
            user=config["user"],
            password=config["password"]
        )
        conn.close()
        print("[OK] Connection successful!")
        return True
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check that the password is correct")
        print("3. Verify PostgreSQL is listening on port", config["port"])
        print("\nIf you forgot your PostgreSQL password, you can reset it:")
        print("  - Find pg_hba.conf file (usually in PostgreSQL data directory)")
        print("  - Temporarily change 'md5' to 'trust' for local connections")
        print("  - Restart PostgreSQL service")
        print("  - Connect without password and reset: ALTER USER postgres PASSWORD 'newpassword';")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


def database_exists(config, db_name):
    """Check if a database exists."""
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname="postgres",
            user=config["user"],
            password=config["password"]
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking database: {e}")
        return False


def create_database(config, db_name):
    """Create a database if it doesn't exist."""
    if database_exists(config, db_name):
        print(f"  Database '{db_name}' already exists")
        return True
    
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname="postgres",
            user=config["user"],
            password=config["password"]
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f'CREATE DATABASE "{db_name}"')
        cur.close()
        conn.close()
        print(f"  [OK] Created database '{db_name}'")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to create database '{db_name}': {e}")
        return False


def run_schema(config, db_name):
    """Run schema.sql on a database."""
    schema_path = Path(__file__).parent / "sql" / "schema.sql"
    
    if not schema_path.exists():
        print(f"  [ERROR] Schema file not found: {schema_path}")
        return False
    
    try:
        conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            dbname=db_name,
            user=config["user"],
            password=config["password"]
        )
        cur = conn.cursor()
        
        # Read and execute schema file
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cur.execute(schema_sql)
        conn.commit()
        cur.close()
        conn.close()
        print(f"  [OK] Initialized schema for '{db_name}'")
        return True
    except Exception as e:
        print(f"  [ERROR] Failed to initialize schema: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main setup function."""
    # Get password from command line if provided
    password = sys.argv[1] if len(sys.argv) > 1 else None
    
    config = get_db_config(password)
    
    if not test_connection(config):
        print("\nPlease fix the connection issue and try again.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Creating databases...")
    print("=" * 60)
    
    databases = ["vacations", "test_db"]
    success = True
    
    for db_name in databases:
        print(f"\nSetting up '{db_name}' database...")
        if not create_database(config, db_name):
            success = False
            continue
        
        if not run_schema(config, db_name):
            success = False
            continue
    
    if success:
        print("\n" + "=" * 60)
        print("[OK] Database setup completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Create a .env file in the backend directory:")
        print("   DB_HOST=localhost")
        print("   DB_PORT=5432")
        print("   DB_NAME=vacations")
        print("   DB_USER=postgres")
        print(f"   DB_PASSWORD={config['password']}")
        print("\n2. Run the tests:")
        print("   python src/main.py")
    else:
        print("\n" + "=" * 60)
        print("[ERROR] Database setup completed with errors")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
