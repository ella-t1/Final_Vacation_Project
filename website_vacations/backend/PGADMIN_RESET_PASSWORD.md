# Reset Password in pgAdmin - Step by Step

## Step 1: Connect to PostgreSQL Server

1. **In pgAdmin, look at the left panel (Object Explorer)**
2. **Find "PostgreSQL 17"** (it has a red X, meaning disconnected)
3. **Right-click on "PostgreSQL 17"**
4. **Click "Connect Server"** (or just double-click it)

5. **If it asks for a password:**
   - Since you changed pg_hba.conf to "trust", you can leave the password **empty**
   - Or try pressing **Connect** without entering anything
   - The server should connect without a password

## Step 2: Navigate to Login/Group Roles

Once connected (the red X should disappear):

1. **Expand "PostgreSQL 17"** (click the arrow/plus icon)
2. **Expand "Login/Group Roles"** folder
3. You should see **"postgres"** listed there

## Step 3: Reset Password

1. **Right-click on "postgres"**
2. **Click "Properties"** (or just double-click "postgres")
3. A properties window will open

4. **Go to the "Definition" tab** (at the top of the properties window)
5. **In the "Password" field**, enter: `123456`
6. **In the "Password (again)" field**, enter: `123456` again
7. **Click "Save"** button (at the bottom)

## Step 4: Done!

The password is now reset to `123456`.

## Step 5: Change pg_hba.conf Back

**IMPORTANT:** Now you need to restore security:

1. **Open:** `E:\DB\pg_hba.conf` in Notepad
2. **Find these lines:**
   ```
   host    all             all             127.0.0.1/32            trust
   host    all             all             ::1/128                 trust
   ```
3. **Change `trust` back to `scram-sha-256`:**
   ```
   host    all             all             127.0.0.1/32            scram-sha-256
   host    all             all             ::1/128                 scram-sha-256
   ```
4. **Save the file**

## Step 6: Test Connection

```powershell
cd backend
py test_postgres_123456.py
```

You should see: `[SUCCESS] All tests passed!`

