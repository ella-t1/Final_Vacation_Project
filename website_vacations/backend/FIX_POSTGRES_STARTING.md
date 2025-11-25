# Fix PostgreSQL Service That Stops Immediately

## Problem
PostgreSQL service starts but immediately stops with error:
"The postgresql-x64-17 service started and then stopped."

## Root Cause
**Syntax error in pg_hba.conf** - The file had BOTH `trust` and `scram-sha-256` on the same line, which is invalid.

## Solution Applied
✅ **Fixed pg_hba.conf** - Changed lines to use only `trust` (for password reset)

## Next Steps

### 1. Start PostgreSQL Service Again

1. **Open Services app:**
   - Press `Win + R`
   - Type: `services.msc`
   - Press Enter

2. **Find:** "postgresql-x64-17 - PostgreSQL Server 17"

3. **Right-click** → **Start**

4. **Wait a few seconds** - it should stay running now!

5. **Check status** - should show "Running" (not "Stopped")

### 2. Connect in pgAdmin

1. **Open pgAdmin**
2. **Right-click "PostgreSQL 17"** → **"Connect Server"**
3. **Leave password empty** (trust mode)
4. **Click Connect**

### 3. Reset Password

1. **Expand "PostgreSQL 17"**
2. **Expand "Login/Group Roles"**
3. **Right-click "postgres"** → **Properties**
4. **Go to "Definition" tab**
5. **Set password:** `123456`
6. **Click Save**

### 4. Restore Security

After resetting password:

1. **Open:** `E:\DB\pg_hba.conf`
2. **Change `trust` back to `scram-sha-256`:**
   ```
   host    all             all             127.0.0.1/32            scram-sha-256
   host    all             all             ::1/128                 scram-sha-256
   ```
3. **Save**
4. **Restart PostgreSQL service**

### 5. Test

```powershell
cd backend
py test_postgres_123456.py
```

## If Service Still Stops

Check PostgreSQL logs:
- Location: `E:\DB\log\` or `E:\DB\pg_log\`
- Look for error messages

Common issues:
- Port 5432 already in use
- Data directory permissions
- Corrupted configuration files

