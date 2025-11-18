"""Test different password and connection options."""

import psycopg2
import sys

def test_connection(host, port, dbname, user, password, description):
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
        print(f"[OK] {description}")
        return True
    except psycopg2.OperationalError as e:
        print(f"[FAIL] {description}: {str(e)[:100]}")
        return False
    except Exception as e:
        print(f"[ERROR] {description}: {str(e)[:100]}")
        return False

if __name__ == "__main__":
    print("Testing PostgreSQL connection with different options...")
    print("=" * 60)
    
    # Common passwords to try
    passwords_to_try = [
        "123456",
        "postgres",
        "admin",
        "password",
        "",  # empty password
    ]
    
    hosts_to_try = ["localhost", "127.0.0.1"]
    databases_to_try = ["postgres", "vacations"]
    
    success = False
    
    for host in hosts_to_try:
        for dbname in databases_to_try:
            for password in passwords_to_try:
                desc = f"host={host}, db={dbname}, password={'*' * len(password) if password else '(empty)'}"
                if test_connection(host, 5432, dbname, "postgres", password, desc):
                    print(f"\n{'=' * 60}")
                    print(f"SUCCESS! Working configuration:")
                    print(f"  DB_HOST={host}")
                    print(f"  DB_NAME={dbname}")
                    print(f"  DB_USER=postgres")
                    print(f"  DB_PASSWORD={password if password else '(empty)'}")
                    print(f"\nUpdate your backend/.env file with these values!")
                    success = True
                    break
            if success:
                break
        if success:
            break
    
    if not success:
        print("\n" + "=" * 60)
        print("None of the common passwords worked.")
        print("\nTROUBLESHOOTING:")
        print("1. Check if PostgreSQL is actually running")
        print("2. Try connecting via pgAdmin or another PostgreSQL client")
        print("3. Check PostgreSQL logs for authentication errors")
        print("4. Verify the PostgreSQL user exists:")
        print("   - Open pgAdmin")
        print("   - Check Server > Login/Group Roles > postgres")
        print("5. You may need to reset the password:")
        print("   - Open Command Prompt as Admin")
        print("   - cd to PostgreSQL bin directory")
        print("   - psql -U postgres")
        print("   - ALTER USER postgres PASSWORD 'newpassword';")
        sys.exit(1)
    else:
        sys.exit(0)

