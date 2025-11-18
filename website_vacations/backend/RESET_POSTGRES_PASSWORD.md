# Reset PostgreSQL Password - Step by Step

Since password authentication is failing, let's reset it properly.

## Method 1: Reset via Command Line (Recommended)

### Step 1: Find PostgreSQL Installation

PostgreSQL is usually installed in:
- `C:\Program Files\PostgreSQL\15\bin` (or version 14, 13, etc.)
- `C:\Program Files\PostgreSQL\16\bin`

### Step 2: Open Command Prompt as Administrator

1. Press `Win + X`
2. Select "Windows PowerShell (Admin)" or "Command Prompt (Admin)"

### Step 3: Navigate to PostgreSQL bin directory

```bash
cd "C:\Program Files\PostgreSQL\15\bin"
```

(Replace `15` with your PostgreSQL version number)

### Step 4: Connect to PostgreSQL

```bash
psql -U postgres
```

**If this asks for a password and you don't know it**, try:
- Press Enter (empty password)
- Or try: `psql -U postgres -d postgres` (might bypass password)

### Step 5: Reset the Password

Once connected (you'll see `postgres=#`), run:

```sql
ALTER USER postgres PASSWORD '123456';
```

Then exit:
```sql
\q
```

### Step 6: Test the Connection

```bash
psql -U postgres -d postgres
```

Enter password `123456` when prompted.

## Method 2: Reset via pgAdmin (If you have it installed)

1. Open **pgAdmin**
2. Connect to your PostgreSQL server (you might need to enter current password)
3. Expand: **Servers** → Your Server → **Login/Group Roles**
4. Right-click on **postgres** → **Properties**
5. Go to **Definition** tab
6. Enter new password: `123456`
7. Click **Save**

## Method 3: Check pg_hba.conf (Advanced)

If password authentication still doesn't work, PostgreSQL might be configured differently.

1. Find `pg_hba.conf` file (usually in PostgreSQL data directory):
   - `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`

2. Look for lines starting with:
   ```
   host    all    all    127.0.0.1/32    md5
   host    all    all    ::1/128         md5
   ```

3. Make sure they use `md5` or `scram-sha-256` (password authentication)

4. If it says `trust`, change it to `md5`:
   ```
   host    all    all    127.0.0.1/32    md5
   ```

5. Restart PostgreSQL service:
   ```bash
   # In PowerShell as Admin
   Restart-Service postgresql-x64-15
   ```
   (Replace `15` with your version)

## Method 4: Use Windows Authentication (Alternative)

If you can't reset the password, you can configure PostgreSQL to use Windows authentication temporarily:

1. Edit `pg_hba.conf`:
   ```
   host    all    all    127.0.0.1/32    trust
   ```

2. Restart PostgreSQL

3. Update `.env` to use your Windows username instead of `postgres`

## Quick Test After Reset

After resetting, test with:

```bash
cd backend
py test_db_connection.py
```

You should see: `[OK] Connection successful!`

## Still Having Issues?

1. **Check PostgreSQL version:**
   ```bash
   # In PostgreSQL bin directory
   psql --version
   ```

2. **Check if PostgreSQL service is running:**
   ```powershell
   Get-Service postgresql*
   ```

3. **Check PostgreSQL logs:**
   - Usually in: `C:\Program Files\PostgreSQL\15\data\log\`
   - Look for authentication errors

4. **Try connecting with a different user:**
   - Create a new user in PostgreSQL
   - Use that user in `.env` instead of `postgres`

