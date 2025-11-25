# Reset Password Without SQL Shell - All Options

Since you've changed pg_hba.conf to "trust", here are all the ways to reset the password:

## Option 1: Python Script (No SQL Shell Needed)

**After restarting PostgreSQL**, run:
```powershell
cd backend
py reset_password_python.py
```

This will connect without password and reset it to 123456.

## Option 2: pgAdmin (GUI - Easiest)

1. **Open pgAdmin 4** from Start Menu
2. **Connect to PostgreSQL server**
   - If it asks for password, leave it empty (trust mode)
3. **Expand:** Servers → Your Server → **Login/Group Roles**
4. **Right-click** on **postgres** → **Properties**
5. Go to **Definition** tab
6. Enter password: `123456`
7. Click **Save**

**No SQL shell needed!**

## Option 3: Use psql.exe (But Easier Than SQL Shell)

If PostgreSQL is running, you can use psql.exe directly:

```powershell
cd "C:\Program Files\PostgreSQL\17\bin"
.\psql.exe -U postgres -c "ALTER USER postgres PASSWORD '123456';"
```

This runs the command directly without opening an interactive shell.

## Option 4: Check if PostgreSQL is Running First

If the Python script says "Connection refused", PostgreSQL might not be running:

1. **Check service status:**
   ```powershell
   Get-Service postgresql-x64-17
   ```

2. **Start it manually:**
   ```powershell
   Start-Service postgresql-x64-17
   ```

3. **Or use Services app:**
   - Press `Win + R`
   - Type: `services.msc`
   - Find "postgresql-x64-17"
   - Right-click → Start

4. **Then try the Python script again:**
   ```powershell
   cd backend
   py reset_password_python.py
   ```

## After Resetting Password

1. **Change pg_hba.conf back:**
   - Open `E:\DB\pg_hba.conf`
   - Change `trust` back to `scram-sha-256`
   - Save

2. **Restart PostgreSQL:**
   ```powershell
   Restart-Service postgresql-x64-17
   ```

3. **Test:**
   ```powershell
   cd backend
   py test_postgres_123456.py
   ```

## Recommended: Use pgAdmin

**pgAdmin is the easiest** - no command line, no file editing after resetting password, just a GUI!

