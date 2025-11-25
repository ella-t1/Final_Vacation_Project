"""Test PostgreSQL connection with password 123456."""

import psycopg2
import os
from dotenv import load_dotenv

def test_connection_with_password(password="123456"):
    """Test PostgreSQL connection with specified password."""
    
    # Load .env if it exists
    load_dotenv()
    
    # Get database configuration
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '5432')),
        'dbname': os.getenv('DB_NAME', 'vacations'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', password),  # Use provided password if .env doesn't exist
    }
    
    # Override password with the one we want to test
    db_config['password'] = password
    
    print("=" * 70)
    print("Testing PostgreSQL Connection")
    print("=" * 70)
    print(f"Host:        {db_config['host']}")
    print(f"Port:        {db_config['port']}")
    print(f"Database:    {db_config['dbname']}")
    print(f"User:        {db_config['user']}")
    print(f"Password:    {'*' * len(password)}")
    print("-" * 70)
    
    try:
        # Attempt to connect
        print("Attempting connection...")
        conn = psycopg2.connect(**db_config)
        print("[OK] Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"[OK] PostgreSQL version: {version[0][:60]}...")
        
        # Test database name
        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"[OK] Connected to database: {db_name[0]}")
        
        # Check if vacations database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'vacations';")
        exists = cursor.fetchone()
        if exists:
            print("[OK] Database 'vacations' exists")
        else:
            print("[WARNING] Database 'vacations' does not exist")
        
        # Close connections
        cursor.close()
        conn.close()
        
        print("-" * 70)
        print("[SUCCESS] All tests passed!")
        print("=" * 70)
        print("\nYour PostgreSQL connection is working correctly!")
        print(f"Password '{password}' is correct.")
        print("\nMake sure your backend/.env file contains:")
        print(f"DB_PASSWORD={password}")
        return True
        
    except psycopg2.OperationalError as e:
        error_msg = str(e)
        print(f"[ERROR] Connection failed!")
        print(f"Error: {error_msg}")
        print("-" * 70)
        
        if "password authentication failed" in error_msg.lower():
            print("\n[DIAGNOSIS] Password authentication failed.")
            print(f"The password '{password}' is incorrect for user 'postgres'.")
            print("\nYou need to reset the PostgreSQL password.")
            return False
        elif "could not connect" in error_msg.lower():
            print("\n[DIAGNOSIS] Cannot connect to PostgreSQL server.")
            print("PostgreSQL might not be running or not accessible.")
            return False
        elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
            print("\n[DIAGNOSIS] Database does not exist.")
            print("You need to create the 'vacations' database.")
            return False
        else:
            print(f"\n[DIAGNOSIS] Unknown error: {error_msg}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\nTesting PostgreSQL connection with password: 123456\n")
    success = test_connection_with_password("123456")
    
    if not success:
        print("\n" + "=" * 70)
        print("NEXT STEPS: Reset PostgreSQL Password")
        print("=" * 70)
        print("\nSee instructions below for resetting the password.\n")
    
    exit(0 if success else 1)

