# Step-by-Step PostgreSQL Setup Guide

## Current Status
✅ PostgreSQL 17 is installed and running
✅ Data directory found at: `E:\DB`
✅ Configuration file found: `E:\DB\pg_hba.conf`

## Step-by-Step Instructions

### Step 1: Reset PostgreSQL Password

Since you never set up a password, we need to create one. I've created a script that will:
1. Temporarily allow passwordless connection
2. Let you set a new password
3. Restore secure authentication

**Run this command in PowerShell (from the backend directory):**
```powershell
.\reset_postgres_password.ps1
```

The script will:
- Prompt you to enter a new password (choose something secure, like `postgres123` or your own password)
- Set the password for the `postgres` user
- Test the connection
- Show you the next steps

### Step 2: Set Up Databases

After setting the password, run the database setup script:
```powershell
py setup_database.py your_password_here
```

Replace `your_password_here` with the password you just set.

This will:
- Create `vacations` database
- Create `test_db` database  
- Initialize the schema (tables, constraints, seed data)

### Step 3: Create .env File

The setup script will create a `.env` file automatically, or you can create it manually:

Create `backend/.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### Step 4: Test Everything

Test the connection:
```powershell
py test_connection.py
```

Run all tests:
```powershell
py src/main.py
```

## Quick Start (All Steps Combined)

If you want to do everything at once:

1. **Set password:**
   ```powershell
   cd backend
   .\reset_postgres_password.ps1
   ```
   (Remember the password you enter!)

2. **Set up databases:**
   ```powershell
   py setup_database.py your_password_here
   ```

3. **Test:**
   ```powershell
   py src/main.py
   ```

## Troubleshooting

### If password reset script fails:
- Make sure you're running PowerShell as Administrator
- Check that PostgreSQL service is running: `Get-Service postgresql-x64-17`
- Try restarting PostgreSQL: `Restart-Service postgresql-x64-17`

### If database setup fails:
- Verify password is correct
- Check that databases were created: `psql -U postgres -l`
- Make sure schema.sql file exists: `backend/sql/schema.sql`

## What Each Script Does

- **reset_postgres_password.ps1**: Safely resets PostgreSQL password
- **setup_database.py**: Creates databases and initializes schema
- **test_connection.py**: Tests database connection
- **src/main.py**: Runs all backend tests

