# Database Setup Guide

This guide will help you set up PostgreSQL for the Vacations project.

## Prerequisites

- PostgreSQL installed and running
- Python 3.x installed
- Dependencies installed (`pip install -r requirements.txt`)

## Quick Setup (Recommended)

### Option 1: Using PowerShell Script (Easiest)

1. Open PowerShell in the `backend` directory
2. Run the setup script:
   ```powershell
   .\setup_database.ps1
   ```
3. Enter your PostgreSQL password when prompted
4. The script will:
   - Create the `vacations` and `test_db` databases
   - Initialize the schema
   - Create a `.env` file with your credentials

### Option 2: Using Python Script

1. Set your PostgreSQL password as an environment variable:
   ```powershell
   $env:DB_PASSWORD="your_postgres_password"
   ```

2. Run the setup script:
   ```powershell
   py setup_database.py
   ```

   Or pass the password directly:
   ```powershell
   py setup_database.py your_postgres_password
   ```

3. Create a `.env` file manually (see below)

## Manual Setup

If you prefer to set up manually:

### Step 1: Find Your PostgreSQL Password

If you don't remember your PostgreSQL password:

**Option A: Check if you saved it somewhere**
- Look for installation notes
- Check password managers

**Option B: Reset PostgreSQL Password**

1. Find PostgreSQL data directory (usually `C:\Program Files\PostgreSQL\<version>\data`)
2. Locate `pg_hba.conf` file
3. Temporarily change authentication method:
   - Find line: `host all all 127.0.0.1/32 md5`
   - Change to: `host all all 127.0.0.1/32 trust`
4. Restart PostgreSQL service:
   ```powershell
   Restart-Service postgresql-x64-<version>
   ```
5. Connect without password:
   ```powershell
   psql -U postgres -d postgres
   ```
6. Reset password:
   ```sql
   ALTER USER postgres PASSWORD 'newpassword';
   ```
7. Revert `pg_hba.conf` back to `md5`
8. Restart PostgreSQL service again

### Step 2: Create Databases

Using psql (if available in PATH):
```powershell
psql -U postgres -c "CREATE DATABASE vacations;"
psql -U postgres -c "CREATE DATABASE test_db;"
```

Or using the setup script (recommended).

### Step 3: Initialize Schema

Using psql:
```powershell
psql -U postgres -d vacations -f sql\schema.sql
psql -U postgres -d test_db -f sql\schema.sql
```

Or the setup script will do this automatically.

### Step 4: Create .env File

Create a file named `.env` in the `backend` directory:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
```

**Important:** Replace `your_actual_password_here` with your actual PostgreSQL password!

## Verify Setup

After setup, test the connection:

```powershell
py test_connection.py
```

Then run the full test suite:

```powershell
py src/main.py
```

## Troubleshooting

### "password authentication failed"
- Verify your PostgreSQL password is correct
- Check that PostgreSQL service is running
- Ensure the `.env` file has the correct password

### "database does not exist"
- Run the setup script to create databases
- Or manually create: `CREATE DATABASE vacations;`

### "relation does not exist"
- Run the schema initialization: `psql -U postgres -d vacations -f sql\schema.sql`
- Or use the setup script which does this automatically

### "could not connect to server"
- Check PostgreSQL service is running: `Get-Service postgresql*`
- Verify PostgreSQL is listening on port 5432
- Check firewall settings

## Need Help?

If you're still having issues:
1. Make sure PostgreSQL is installed and running
2. Verify you know your PostgreSQL admin password
3. Check that port 5432 is not blocked
4. Try connecting manually: `psql -U postgres -d postgres`

