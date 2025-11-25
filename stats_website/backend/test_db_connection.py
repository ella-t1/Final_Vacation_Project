"""Test PostgreSQL database connection."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_connection():
    """Test database connection."""
    try:
        from src.config import get_connection_kwargs
        import psycopg2
        
        print("Testing PostgreSQL connection...")
        print("=" * 50)
        
        # Get connection parameters
        conn_kwargs = get_connection_kwargs()
        print(f"Host: {conn_kwargs['host']}")
        print(f"Port: {conn_kwargs['port']}")
        print(f"Database: {conn_kwargs['dbname']}")
        print(f"User: {conn_kwargs['user']}")
        print("=" * 50)
        
        # Try to connect
        print("\nAttempting to connect...")
        conn = psycopg2.connect(**conn_kwargs)
        
        # Test query
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"✓ Connected successfully!")
            print(f"✓ PostgreSQL version: {version[0]}")
            
            # Check if database has required tables
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cur.fetchall()
            print(f"\n✓ Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Check for required tables
            required_tables = ['users', 'roles', 'vacations', 'likes', 'countries']
            existing_tables = [t[0] for t in tables]
            missing_tables = [t for t in required_tables if t not in existing_tables]
            
            if missing_tables:
                print(f"\n⚠ Warning: Missing tables: {missing_tables}")
            else:
                print("\n✓ All required tables exist!")
            
            # Check admin user
            cur.execute("""
                SELECT u.id, u.username, u.email, r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE r.name = 'Admin'
                LIMIT 1;
            """)
            admin = cur.fetchone()
            if admin:
                print(f"\n✓ Admin user found: {admin[1]} ({admin[2]})")
            else:
                print("\n⚠ Warning: No admin user found!")
        
        conn.close()
        print("\n" + "=" * 50)
        print("✅ Database connection test PASSED!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ Connection failed!")
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check database credentials in .env file or environment variables")
        print("3. Verify database 'vacations' exists")
        print("4. Check if PostgreSQL is listening on the correct port")
        return False
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        print("Make sure psycopg2-binary is installed:")
        print("  py -m pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

