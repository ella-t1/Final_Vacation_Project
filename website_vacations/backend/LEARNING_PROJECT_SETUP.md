# Learning Project Setup - No Password Option

Since this is a learning project, you can keep PostgreSQL in "trust" mode (no password required).

## Current Status
✅ PostgreSQL is connected in pgAdmin
✅ pg_hba.conf is set to "trust" mode (no password needed)

## Option 1: Keep No Password (Recommended for Learning)

### Keep Current Setup
- **pg_hba.conf:** Already set to `trust` - **KEEP IT AS IS**
- **No password needed** for any connections
- **Perfect for learning!**

### Update backend/.env
Create or update `backend/.env`:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=
```

**Note:** `DB_PASSWORD=` is empty (or you can omit it entirely)

### Test Connection
```powershell
cd backend
py test_postgres_123456.py
```

**Note:** Even though the test script expects a password, with "trust" mode, PostgreSQL will accept empty password.

## Option 2: Set Password But Keep Trust Mode

If you want to set a password (for learning purposes) but still use trust mode:

### In pgAdmin:
1. **Expand "localhost"** → **"Login/Group Roles"**
2. **Right-click "postgres"** → **Properties**
3. **Go to "Definition" tab**
4. **Set password:** `123456`
5. **Click Save**

### Keep pg_hba.conf as "trust"
- **Don't change pg_hba.conf back to scram-sha-256**
- Keep it as `trust` so password won't be checked
- This way you have a password set, but trust mode bypasses it

### Update backend/.env
```
DB_PASSWORD=123456
```

(Even though trust mode won't check it, having it in .env is good practice)

## Option 3: Full Security (For Production Later)

**Only if you want to practice with password authentication:**

1. **Set password in pgAdmin** (as in Option 2)
2. **Change pg_hba.conf back to scram-sha-256:**
   ```
   host    all             all             127.0.0.1/32            scram-sha-256
   host    all             all             ::1/128                 scram-sha-256
   ```
3. **Restart PostgreSQL service**
4. **Update backend/.env:** `DB_PASSWORD=123456`

## Recommendation for Learning Project

**Use Option 1** - Keep trust mode, no password needed. It's simpler and perfect for learning!

## Summary

**For learning project:**
- ✅ Keep `trust` in pg_hba.conf (no password needed)
- ✅ Set `DB_PASSWORD=` (empty) in backend/.env
- ✅ Everything will work without passwords
- ✅ Simple and easy for learning!

