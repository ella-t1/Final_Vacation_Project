# Fix PostgreSQL Password Authentication Error

## Problem
The error `password authentication failed for user "postgres"` means the password in your `.env` file doesn't match your actual PostgreSQL password.

## Solution

### Step 1: Find Your PostgreSQL Password

You need to know the password you set when installing PostgreSQL, or reset it if you forgot.

### Step 2: Update the .env File

Edit the file: `backend/.env`

Change this line:
```
DB_PASSWORD=123456
```

To your actual PostgreSQL password:
```
DB_PASSWORD=your_actual_postgres_password
```

**Important:** Replace `your_actual_postgres_password` with your real PostgreSQL password!

### Step 3: Restart the Backend

After updating the `.env` file:

1. Stop the backend (Ctrl+C in the terminal where it's running)
2. Start it again:
   ```bash
   cd backend
   py run_api.py
   ```

### Step 4: Test the Connection

Run the test script:
```bash
cd backend
py test_db_connection.py
```

You should see: `[OK] Connection successful!`

## If You Don't Know Your PostgreSQL Password

### Option 1: Reset PostgreSQL Password (Windows)

1. Open Command Prompt as Administrator
2. Navigate to PostgreSQL bin directory (usually):
   ```bash
   cd "C:\Program Files\PostgreSQL\15\bin"
   ```
   (Replace `15` with your PostgreSQL version)
3. Reset password:
   ```bash
   psql -U postgres
   ```
   Then in psql:
   ```sql
   ALTER USER postgres PASSWORD 'newpassword';
   \q
   ```

### Option 2: Check PostgreSQL Configuration

If you're using pgAdmin or another PostgreSQL tool, check what password you're using there.

### Option 3: Use Windows Authentication

If PostgreSQL is configured for Windows authentication, you might need to change the connection method in `pg_hba.conf`.

## Quick Fix Summary

1. Edit `backend/.env`
2. Change `DB_PASSWORD=123456` to your real password
3. Restart backend: `py run_api.py`
4. Try registering again in the frontend

