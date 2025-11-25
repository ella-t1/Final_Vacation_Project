# Backend Testing Setup Guide

## Prerequisites
- Python 3.x installed (use `py` command on Windows)
- PostgreSQL database running
- Database should have the vacations schema from Part II

## Step 1: Install Dependencies

### Option A: Using Virtual Environment (Recommended)
```bash
cd stats_website/backend

# Create virtual environment
py -m venv venv

# Activate virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows CMD:
.\venv\Scripts\activate.bat
# On Git Bash:
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Install Globally (Not Recommended)
```bash
cd stats_website/backend
py -m pip install -r requirements.txt
```

## Step 2: Configure Environment Variables

Create a `.env` file in `stats_website/backend/` (optional, defaults will be used):

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=postgres
FLASK_PORT=5001
FLASK_DEBUG=True
```

## Step 3: Verify Database Connection

Make sure PostgreSQL is running and the `vacations` database exists with the schema from Part II.

## Step 4: Test Backend

### Test 1: Verify Imports
```bash
cd stats_website/backend
py test_backend.py
```

Expected output:
```
✓ Config module imported successfully
✓ All DAO modules imported successfully
✓ All service modules imported successfully
✓ All API modules imported successfully

✅ All imports successful! Backend structure is correct.
```

### Test 2: Run the Server
```bash
cd stats_website/backend
py run_api.py
```

Expected output:
```
Starting Statistics API server on http://localhost:5001
API endpoints available at http://localhost:5001/
...
 * Running on http://0.0.0.0:5001
```

### Test 3: Test Endpoints

Open a new terminal and test the endpoints:

#### Health Check (No auth required)
```bash
curl http://localhost:5001/health
```

Expected response:
```json
{"status":"ok"}
```

#### Login (Admin only)
```bash
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin1234\"}" \
  -c cookies.txt -v
```

Expected response (success):
```json
{
  "id": 1,
  "firstName": "Admin",
  "lastName": "User",
  "email": "admin@vacations.com",
  "username": "admin",
  "roleId": 1
}
```

Expected response (non-admin):
```json
{"error":"Admin access required"}
```

#### Get Statistics (Requires auth - use cookies from login)
```bash
# Vacation stats
curl http://localhost:5001/vacations/stats -b cookies.txt

# Total users
curl http://localhost:5001/users/total -b cookies.txt

# Total likes
curl http://localhost:5001/likes/total -b cookies.txt

# Likes distribution
curl http://localhost:5001/likes/distribution -b cookies.txt
```

#### Logout
```bash
curl -X POST http://localhost:5001/logout -b cookies.txt
```

## Troubleshooting

### Issue: "pip: command not found"
**Solution:** Use `py -m pip` instead of `pip`

### Issue: "Module not found" errors
**Solution:** 
1. Make sure you're in the `stats_website/backend` directory
2. Activate virtual environment if using one
3. Install dependencies: `py -m pip install -r requirements.txt`

### Issue: Database connection errors
**Solution:**
1. Verify PostgreSQL is running
2. Check database credentials in `.env` or environment variables
3. Verify database `vacations` exists
4. Verify schema is loaded (from Part II)

### Issue: "Admin access required" even with admin user
**Solution:**
1. Check database - verify user has `role_id = 1` (Admin role)
2. Check role name in database: `SELECT * FROM roles WHERE id = 1;` should return name = 'Admin'
3. Verify password matches: `SELECT * FROM users WHERE username = 'admin';`

### Issue: Port already in use
**Solution:** 
1. Change port in `.env`: `FLASK_PORT=5002`
2. Or stop the other service using port 5001

## Expected Test Results

After successful setup:
- ✅ All imports work
- ✅ Server starts without errors
- ✅ Health endpoint returns `{"status":"ok"}`
- ✅ Login with admin credentials succeeds
- ✅ Login with non-admin fails with "Admin access required"
- ✅ Statistics endpoints return data when authenticated
- ✅ Statistics endpoints return 401 when not authenticated
- ✅ Logout clears session

