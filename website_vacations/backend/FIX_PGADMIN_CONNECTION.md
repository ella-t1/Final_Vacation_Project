# Fix pgAdmin Connection Error

## Problem
The error "[Errno 11001] getaddrinfo failed" means pgAdmin can't find the server "ella".

## Solution: Change Hostname

In the pgAdmin connection dialog:

1. **Change "Host name/address" from "ella" to:**
   ```
   localhost
   ```
   OR
   ```
   127.0.0.1
   ```

2. **Keep these settings:**
   - Port: `5432`
   - Maintenance database: `postgres`
   - Username: `postgres`
   - Password: **Leave EMPTY** (trust mode allows this)

3. **Click "Save"** (or "Test Connection" first to verify)

4. **Then try connecting again**

## Step-by-Step

1. In the "Register - Server" dialog:
   - **Host name/address:** Change `ella` to `localhost`
   - **Port:** `5432` (should already be correct)
   - **Username:** `postgres` (should already be correct)
   - **Password:** Leave EMPTY
   - Click **"Save"**

2. After saving, the server should appear in the left panel

3. **Right-click "PostgreSQL 17"** → **"Connect Server"**

4. If it asks for password, leave it empty and click Connect

5. Once connected, follow the password reset steps

