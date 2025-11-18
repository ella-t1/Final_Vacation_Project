# Quick Password Reset Steps

## File Location
**pg_hba.conf is at:** `E:\DB\pg_hba.conf`

## Easy Way to Open It

**Option 1: Double-click this file:**
- `backend\open_pg_hba.bat` (opens the file automatically)

**Option 2: Open manually:**
1. Press `Win + R`
2. Type: `notepad E:\DB\pg_hba.conf`
3. Press Enter

**Option 3: File Explorer:**
1. Open File Explorer
2. Go to: `E:\DB\`
3. Find `pg_hba.conf`
4. Right-click → Open with → Notepad

## Step-by-Step Reset

### Step 1: Edit pg_hba.conf

1. **Open the file** (use one of the methods above)

2. **Find these lines** (around line 90-95, use Ctrl+F to search for "127.0.0.1"):
   ```
   host    all             all             127.0.0.1/32            scram-sha-256
   host    all             all             ::1/128                 scram-sha-256
   ```

3. **Change `scram-sha-256` to `trust`**:
   ```
   host    all             all             127.0.0.1/32            trust
   host    all             all             ::1/128                 trust
   ```

4. **Save the file** (Ctrl+S)

### Step 2: Restart PostgreSQL

Open PowerShell as Administrator and run:
```powershell
Restart-Service postgresql-x64-17
```

Or use Services app:
- Press `Win + R`
- Type: `services.msc`
- Find "postgresql-x64-17"
- Right-click → Restart

### Step 3: Reset Password

Open PowerShell (or Command Prompt):
```powershell
cd "C:\Program Files\PostgreSQL\17\bin"
.\psql.exe -U postgres -c "ALTER USER postgres PASSWORD '123456';"
```

### Step 4: Restore Security

1. **Edit pg_hba.conf again**
2. **Change `trust` back to `scram-sha-256`**:
   ```
   host    all             all             127.0.0.1/32            scram-sha-256
   host    all             all             ::1/128                 scram-sha-256
   ```
3. **Save**

### Step 5: Restart PostgreSQL Again

```powershell
Restart-Service postgresql-x64-17
```

### Step 6: Test

```powershell
cd "E:\Full Stack + Python (John Bryce)\Lessons-uriel\Final Project\website_vacations\backend"
py test_postgres_123456.py
```

You should see: `[SUCCESS] All tests passed!`

## Alternative: Use pgAdmin (No File Editing)

If you have pgAdmin installed:

1. Open **pgAdmin 4** from Start Menu
2. Connect to PostgreSQL server
3. Expand: **Servers** → Your Server → **Login/Group Roles**
4. Right-click **postgres** → **Properties**
5. Go to **Definition** tab
6. Set password: `123456`
7. Click **Save**

Then test:
```powershell
cd backend
py test_postgres_123456.py
```

