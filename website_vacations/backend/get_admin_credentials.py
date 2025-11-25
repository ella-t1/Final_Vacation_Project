"""Get admin credentials from database."""

import psycopg2

def get_admin_credentials():
    """Get admin user credentials."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="vacations",
            user="postgres",
            password=""  # Empty password with trust mode
        )
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, first_name, last_name, email, password, role_id FROM users WHERE role_id = 1"
        )
        admin = cursor.fetchone()
        
        if admin:
            print("=" * 60)
            print("ADMIN CREDENTIALS")
            print("=" * 60)
            print()
            print(f"Email:    {admin[3]}")
            print(f"Password: {admin[4]}")
            print(f"Full Name: {admin[1]} {admin[2]}")
            print(f"Role ID:  {admin[5]} (Admin)")
            print()
            print("=" * 60)
        else:
            print("No admin user found!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_admin_credentials()

