# How to Reset PostgreSQL Password

## Test Result
❌ **Password `123456` is NOT working** - Authentication failed

## Method 1: Reset via Command Line (Recommended)

### Step 1: Find PostgreSQL Installation

PostgreSQL is usually installed in one of these locations:
- `C:\Program Files\PostgreSQL\15\bin`
- `C:\Program Files\PostgreSQL\16\bin`
- `C:\Program Files\PostgreSQL\17\bin`

**Find your version:**
```powershell
Get-ChildItem "C:\Program Files\PostgreSQL\" -Directory
```

### Step 2: Open Command Prompt as Administrator

1. Press `Win + X`
2. Select **"Windows PowerShell (Admin)"** or **"Command Prompt (Admin)"**

### Step 3: Navigate to PostgreSQL bin Directory

```powershell
cd "C:\Program Files\PostgreSQL\15\bin"
```

(Replace `15` with your PostgreSQL version number)

### Step 4: Connect to PostgreSQL

Try connecting without password first:
```powershell
.\psql.exe -U postgres
```

**If this asks for a password:**
- Try pressing **Enter** (empty password)
- Or try: `.\psql.exe -U postgres -d postgres`

**If you still can't connect**, you may need to temporarily modify `pg_hba.conf` (see Method 3 below).

### Step 5: Reset the Password

Once connected (you'll see `postgres=#` prompt), run:

```sql
ALTER USER postgres PASSWORD '123456';
```

Then exit:
```sql
\q
```

### Step 6: Test the New Password

```powershell
.\psql.exe -U postgres -d postgres
```

Enter password `123456` when prompted.

## Method 2: Reset via pgAdmin (If Installed)

1. **Open pgAdmin**
2. **Connect to your PostgreSQL server**
   - If it asks for password, try what you remember or leave empty
3. **Expand:** Servers → Your Server → **Login/Group Roles**
4. **Right-click** on **postgres** → **Properties**
5. Go to **Definition** tab
6. Enter new password: `123456`
7. Click **Save**

## Method 3: Reset via pg_hba.conf (If Methods 1 & 2 Don't Work)

If you can't connect at all, temporarily allow passwordless connections:

### Step 1: Find pg_hba.conf

Usually located in:
- `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`
- Or check PostgreSQL data directory

**Find data directory:**
```powershell
Get-ChildItem "C:\Program Files\PostgreSQL\" -Recurse -Filter "pg_hba.conf" | Select-Object FullName
```

### Step 2: Edit pg_hba.conf

1. **Open as Administrator** (Right-click → Run as Administrator)
2. **Find these lines:**
   ```
   host    all    all    127.0.0.1/32    md5
   host    all    all    ::1/128         md5
   ```

3. **Temporarily change to `trust`** (allows no password):
   ```
   host    all    all    127.0.0.1/32    trust
   host    all    all    ::1/128         trust
   ```

4. **Save the file**

### Step 3: Restart PostgreSQL Service

```powershell
# Find PostgreSQL service name
Get-Service postgresql*

# Restart it (replace with your service name)
Restart-Service postgresql-x64-15
```

### Step 4: Connect and Reset Password

Now you should be able to connect without password:

```powershell
cd "C:\Program Files\PostgreSQL\15\bin"
.\psql.exe -U postgres
```

Then reset password:
```sql
ALTER USER postgres PASSWORD '123456';
\q
```

### Step 5: Restore Security

**IMPORTANT:** Change `pg_hba.conf` back to `md5`:

```
host    all    all    127.0.0.1/32    md5
host    all    all    ::1/128         md5
```

**Restart PostgreSQL again:**
```powershell
Restart-Service postgresql-x64-15
```

## Method 4: Quick PowerShell Script

Save this as `reset_postgres_password.ps1` in the backend directory:

```powershell
# Find PostgreSQL installation
$pgPaths = @(
    "C:\Program Files\PostgreSQL\17\bin",
    "C:\Program Files\PostgreSQL\16\bin",
    "C:\Program Files\PostgreSQL\15\bin",
    "C:\Program Files\PostgreSQL\14\bin"
)

$psqlPath = $null
foreach ($path in $pgPaths) {
    if (Test-Path "$path\psql.exe") {
        $psqlPath = $path
        break
    }
}

if (-not $psqlPath) {
    Write-Host "PostgreSQL not found in common locations."
    Write-Host "Please find psql.exe manually and run:"
    Write-Host "  cd 'path\to\postgresql\bin'"
    Write-Host "  .\psql.exe -U postgres"
    Write-Host "  ALTER USER postgres PASSWORD '123456';"
    exit 1
}

Write-Host "Found PostgreSQL at: $psqlPath"
Write-Host "Attempting to reset password..."
Write-Host ""

cd $psqlPath
.\psql.exe -U postgres -c "ALTER USER postgres PASSWORD '123456';"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Password has been reset to: 123456"
    Write-Host ""
    Write-Host "Now test the connection:"
    Write-Host "  cd backend"
    Write-Host "  py test_postgres_123456.py"
} else {
    Write-Host ""
    Write-Host "Failed to reset password automatically."
    Write-Host "Try Method 3 (pg_hba.conf) or connect via pgAdmin."
}
```

Run it:
```powershell
cd backend
.\reset_postgres_password.ps1
```

## After Resetting Password

1. **Update .env file** in `backend/.env`:
   ```
   DB_PASSWORD=123456
   ```

2. **Test the connection:**
   ```powershell
   cd backend
   py test_postgres_123456.py
   ```

3. **You should see:** `[SUCCESS] All tests passed!`

## Troubleshooting

### "psql: command not found"
- Use full path: `"C:\Program Files\PostgreSQL\15\bin\psql.exe"`
- Or add PostgreSQL bin to PATH

### "Permission denied" when editing pg_hba.conf
- Right-click Notepad → Run as Administrator
- Or use: `notepad "C:\Program Files\PostgreSQL\15\data\pg_hba.conf"` (as Admin)

### "Service not found"
- Check service name: `Get-Service postgresql*`
- Use the exact service name shown

### Still can't connect?
- Check if PostgreSQL is running: `Get-Service postgresql*`
- Check port 5432: `netstat -an | findstr 5432`
- Check PostgreSQL logs for errors

## Quick Summary

**Easiest method:**
1. Open PowerShell as Admin
2. `cd "C:\Program Files\PostgreSQL\15\bin"` (replace 15 with your version)
3. `.\psql.exe -U postgres`
4. `ALTER USER postgres PASSWORD '123456';`
5. `\q`
6. Test: `cd backend` → `py test_postgres_123456.py`

