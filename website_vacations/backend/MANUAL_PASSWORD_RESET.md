# Manual PostgreSQL Password Reset - Step by Step

## Current Problem
PostgreSQL can't load `pg_hba.conf` - the file might have a syntax error.

## Solution: Manual Reset via pgAdmin (EASIEST)

### Option 1: Use pgAdmin (Recommended)

1. **Open pgAdmin**
   - Usually installed with PostgreSQL
   - Look for it in Start Menu: "pgAdmin 4"

2. **Connect to PostgreSQL Server**
   - When pgAdmin opens, it will ask for the master password (for pgAdmin itself)
   - Then you'll see your PostgreSQL server
   - **Right-click** on the server → **Properties**
   - Go to **Connection** tab
   - Enter password if needed (try leaving empty or what you remember)

3. **Reset Password**
   - Expand: **Servers** → Your Server → **Login/Group Roles**
   - **Right-click** on **postgres** → **Properties**
   - Go to **Definition** tab
   - Enter new password: `123456`
   - Click **Save**

4. **Test**
   ```powershell
   cd backend
   py test_postgres_123456.py
   ```

## Option 2: Fix pg_hba.conf Manually

### Step 1: Restore from Backup

The script created a backup. Restore it:

```powershell
# Find the backup file
Get-ChildItem "E:\DB\pg_hba.conf.backup_*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Restore it (replace with actual backup filename)
Copy-Item "E:\DB\pg_hba.conf.backup_20251118_125359" "E:\DB\pg_hba.conf" -Force
```

### Step 2: Edit pg_hba.conf Properly

1. **Open Notepad as Administrator**
   - Press `Win + R`
   - Type: `notepad`
   - Right-click Notepad → Run as Administrator

2. **Open the file:**
   ```
   E:\DB\pg_hba.conf
   ```

3. **Find these lines** (around line 90-95):
   ```
   host    all             all             127.0.0.1/32            scram-sha-256
   host    all             all             ::1/128                 scram-sha-256
   ```

4. **Temporarily change to `trust`**:
   ```
   host    all             all             127.0.0.1/32            trust
   host    all             all             ::1/128                 trust
   ```

5. **IMPORTANT:** Make sure:
   - No extra spaces
   - Tabs/spaces are consistent
   - File ends with a newline
   - No syntax errors

6. **Save the file**

### Step 3: Restart PostgreSQL

```powershell
Restart-Service postgresql-x64-17
```

### Step 4: Reset Password

```powershell
cd "C:\Program Files\PostgreSQL\17\bin"
.\psql.exe -U postgres -c "ALTER USER postgres PASSWORD '123456';"
```

### Step 5: Restore Security

1. Edit `pg_hba.conf` again
2. Change `trust` back to `scram-sha-256` (or `md5`)
3. Save
4. Restart PostgreSQL: `Restart-Service postgresql-x64-17`

### Step 6: Test

```powershell
cd backend
py test_postgres_123456.py
```

## Option 3: Check File Syntax

If PostgreSQL still can't load the file, check for syntax errors:

```powershell
# Check file encoding
Get-Content "E:\DB\pg_hba.conf" -Encoding UTF8 | Out-File "E:\DB\pg_hba_fixed.conf" -Encoding UTF8

# Check for common issues
Get-Content "E:\DB\pg_hba.conf" | Select-String -Pattern "^\s*host" | ForEach-Object {
    if ($_ -notmatch "^\s*host\s+\w+\s+\w+\s+\S+\s+\w+$") {
        Write-Host "Potential issue: $_" -ForegroundColor Yellow
    }
}
```

## Quick Summary

**Easiest:** Use pgAdmin to reset password (no file editing needed)

**If pgAdmin doesn't work:** 
1. Restore backup of pg_hba.conf
2. Edit carefully (change scram-sha-256 to trust)
3. Restart PostgreSQL
4. Reset password
5. Change back to scram-sha-256
6. Restart again

