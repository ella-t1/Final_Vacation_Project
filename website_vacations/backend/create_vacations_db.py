"""Create vacations database and initialize schema."""

import psycopg2
from pathlib import Path

def create_database():
    """Create vacations database if it doesn't exist."""
    
    print("=" * 60)
    print("Creating Vacations Database")
    print("=" * 60)
    print()
    
    try:
        # Connect to postgres database
        print("Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="postgres",
            user="postgres",
            password=""  # Empty password with trust mode
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("[OK] Connected!")
        print()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'vacations'")
        exists = cursor.fetchone()
        
        if exists:
            print("[INFO] Database 'vacations' already exists")
            print("Skipping creation...")
        else:
            print("Creating database 'vacations'...")
            cursor.execute("CREATE DATABASE vacations")
            print("[OK] Database 'vacations' created!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to create database: {e}")
        return False

def initialize_schema():
    """Initialize database schema from schema.sql file."""
    
    print()
    print("=" * 60)
    print("Initializing Database Schema")
    print("=" * 60)
    print()
    
    # Read schema.sql file
    schema_file = Path(__file__).parent / "sql" / "schema.sql"
    
    if not schema_file.exists():
        print(f"[ERROR] Schema file not found: {schema_file}")
        return False
    
    print(f"Reading schema file: {schema_file}")
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    try:
        # Connect to vacations database
        print("Connecting to 'vacations' database...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="vacations",
            user="postgres",
            password=""  # Empty password with trust mode
        )
        cursor = conn.cursor()
        print("[OK] Connected!")
        print()
        
        # Execute schema
        print("Executing schema.sql...")
        cursor.execute(schema_sql)
        conn.commit()
        print("[OK] Schema initialized successfully!")
        print()
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"[OK] Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize schema: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print()
    
    # Create database
    if not create_database():
        return 1
    
    # Initialize schema
    if not initialize_schema():
        return 1
    
    print()
    print("=" * 60)
    print("[SUCCESS] Database setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Test connection: py test_postgres_123456.py")
    print("2. Run backend API: py run_api.py")
    print("3. Start frontend: cd ../frontend && npm run dev")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())

