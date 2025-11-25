"""Reset PostgreSQL password using Python (no SQL shell needed)."""

import psycopg2

def reset_password():
    """Reset PostgreSQL password to 123456."""
    
    print("=" * 60)
    print("Resetting PostgreSQL Password")
    print("=" * 60)
    print()
    
    # Connect without password (trust authentication)
    try:
        print("Connecting to PostgreSQL (no password needed with 'trust' mode)...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="postgres",
            user="postgres",
            password=""  # Empty password should work with 'trust'
        )
        print("[OK] Connected successfully!")
        print()
        
        # Reset password
        print("Resetting password to: 123456")
        cursor = conn.cursor()
        cursor.execute("ALTER USER postgres PASSWORD '123456';")
        conn.commit()
        cursor.close()
        conn.close()
        
        print("[SUCCESS] Password has been reset to: 123456")
        print()
        print("=" * 60)
        print("Next steps:")
        print("1. Change 'trust' back to 'scram-sha-256' in pg_hba.conf")
        print("2. Restart PostgreSQL service")
        print("3. Test connection: py test_postgres_123456.py")
        print("=" * 60)
        return True
        
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Connection failed: {e}")
        print()
        print("Make sure:")
        print("1. PostgreSQL service is running")
        print("2. pg_hba.conf has 'trust' for localhost connections")
        print("3. You restarted PostgreSQL after changing pg_hba.conf")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = reset_password()
    exit(0 if success else 1)

