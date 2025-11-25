"""Simple script to test database connection and basic operations."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.config import DbConfig, get_connection_kwargs
from src.dal.role_dao import RoleDAO
from src.dal.user_dao import UserDAO
from src.dal.country_dao import CountryDAO
from src.dal.vacation_dao import VacationDAO


def test_connection() -> bool:
    """Test basic database connection."""
    try:
        import psycopg2
        conn_kwargs = get_connection_kwargs()
        print(f"Attempting to connect to database '{conn_kwargs['dbname']}'...")
        conn = psycopg2.connect(**conn_kwargs)
        conn.close()
        print("[OK] Database connection successful!")
        return True
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Connection failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your environment variables:")
        print(f"   DB_HOST={os.getenv('DB_HOST', 'localhost')}")
        print(f"   DB_PORT={os.getenv('DB_PORT', '5432')}")
        print(f"   DB_NAME={os.getenv('DB_NAME', 'vacations')}")
        print(f"   DB_USER={os.getenv('DB_USER', 'postgres')}")
        print("3. Verify the database exists: createdb vacations")
        print("4. Check PostgreSQL is accessible: psql -U postgres -l")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False


def test_tables_exist() -> bool:
    """Test that required tables exist."""
    try:
        import psycopg2
        conn_kwargs = get_connection_kwargs()
        conn = psycopg2.connect(**conn_kwargs)
        cur = conn.cursor()
        
        tables = ['roles', 'users', 'countries', 'vacations', 'likes']
        missing_tables = []
        
        for table in tables:
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table,))
            exists = cur.fetchone()[0]
            if not exists:
                missing_tables.append(table)
        
        cur.close()
        conn.close()
        
        if missing_tables:
            print(f"[ERROR] Missing tables: {', '.join(missing_tables)}")
            print("   Run the schema.sql script to create tables:")
            print(f"   psql -U {conn_kwargs['user']} -d {conn_kwargs['dbname']} -f backend/sql/schema.sql")
            return False
        else:
            print("[OK] All required tables exist!")
            return True
    except Exception as e:
        print(f"[ERROR] Error checking tables: {e}")
        return False


def test_dao_operations() -> bool:
    """Test basic DAO operations."""
    try:
        print("\nTesting DAO operations...")
        
        # Test RoleDAO
        role_dao = RoleDAO()
        roles = list(role_dao.list_all())
        print(f"[OK] RoleDAO: Found {len(roles)} roles")
        
        # Test CountryDAO
        country_dao = CountryDAO()
        countries = list(country_dao.list_all())
        print(f"[OK] CountryDAO: Found {len(countries)} countries")
        
        # Test UserDAO
        user_dao = UserDAO()
        users = list(user_dao.list_all())
        print(f"[OK] UserDAO: Found {len(users)} users")
        
        # Test VacationDAO
        vacation_dao = VacationDAO()
        vacations = list(vacation_dao.list_all())
        print(f"[OK] VacationDAO: Found {len(vacations)} vacations")
        
        return True
    except Exception as e:
        print(f"[ERROR] DAO operations failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main() -> int:
    """Main function to test database connection and setup."""
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    cfg = DbConfig.from_env()
    
    print(f"\nConfiguration:")
    print(f"  Host: {cfg.host}")
    print(f"  Port: {cfg.port}")
    print(f"  Database: {cfg.name}")
    print(f"  User: {cfg.user}")
    print()
    
    # Test connection
    if not test_connection():
        return 1
    
    # Test tables exist
    if not test_tables_exist():
        return 1
    
    # Test DAO operations
    if not test_dao_operations():
        return 1
    
    print("\n" + "=" * 60)
    print("[OK] All connection tests passed!")
    print("=" * 60)
    print("\nYou can now run the full test suite:")
    print("  python backend/src/main.py")
    print("  OR")
    print("  pytest backend/tests/ -v")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

