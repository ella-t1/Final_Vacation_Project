"""Test database connection with different passwords."""

import psycopg2
import sys

def test_connection(host, port, dbname, user, password):
    """Test PostgreSQL connection."""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        conn.close()
        return True, "Connection successful!"
    except psycopg2.OperationalError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    print("Testing PostgreSQL connection...")
    print("=" * 50)
    
    # Test with password from .env
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    dbname = os.getenv("DB_NAME", "vacations")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Database: {dbname}")
    print(f"User: {user}")
    print(f"Password: {'*' * len(password)}")
    print("-" * 50)
    
    success, message = test_connection(host, port, dbname, user, password)
    
    if success:
        print("[OK] Connection successful!")
        sys.exit(0)
    else:
        print("[ERROR] Connection failed!")
        print(f"Error: {message}")
        print("\n" + "=" * 50)
        print("TROUBLESHOOTING:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check if the password in .env file is correct")
        print("3. Try connecting manually:")
        print(f"   psql -U {user} -h {host} -d {dbname}")
        print("\nTo update password in .env file:")
        print("   Edit backend/.env and set DB_PASSWORD=your_actual_password")
        sys.exit(1)

