# Vacations Backend Project

Complete backend implementation with database, DAL, and business logic layer.

## What's Here

- **src/config.py**: DB connection configuration via environment variables
- **src/dal/**: Data Access Layer with DAOs for all tables (RoleDAO, UserDAO, CountryDAO, VacationDAO, LikeDAO)
- **src/models/dtos.py**: Data Transfer Objects and enums
- **src/services/**: Business logic layer (UserService, VacationService)
- **tests/**: Comprehensive test suite with positive and negative tests
- **sql/schema.sql**: Complete database schema with tables, constraints, and seed data
- **requirements.txt**: Python dependencies

## Quick Start Guide

### Step 1: Install PostgreSQL

Make sure PostgreSQL is installed and running on your system.

### Step 2: Create Virtual Environment

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# If PowerShell execution policy blocks, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Create Databases

```powershell
# Create main database
createdb -U postgres vacations

# Create test database
createdb -U postgres test_db
```

### Step 5: Initialize Database Schema

```powershell
# Initialize main database
psql -U postgres -d vacations -f sql\schema.sql

# Initialize test database
psql -U postgres -d test_db -f sql\schema.sql
```

### Step 6: Set Environment Variables

**Option A: PowerShell (temporary, for current session)**
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="vacations"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password_here"
```

**Option B: Create .env file (recommended)**
```powershell
# Create .env file in backend directory
# Copy the example and update with your values
```

Create `backend/.env` file:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### Step 7: Test Database Connection

```powershell
# Test connection and verify setup
python test_connection.py
```

This will:
- ✓ Test database connection
- ✓ Verify all tables exist
- ✓ Test basic DAO operations
- ✓ Show troubleshooting tips if something fails

### Step 8: Run Tests

**Option A: Run via main.py (runs all tests)**
```powershell
python src\main.py
```

**Option B: Run pytest directly**
```powershell
# For main database tests
pytest tests\ -v

# For test_db (set environment first)
$env:DB_NAME="test_db"
pytest tests\ -v
```

## Testing Workflow

### 1. Test Database Connection First

Always start by testing the connection:

```powershell
python test_connection.py
```

### 2. Run Full Test Suite

```powershell
python src\main.py
```

This will:
- Load environment variables
- Display database configuration
- Run all tests (positive and negative)
- Show test results

### 3. Run Specific Test Files

```powershell
# Test user service only
pytest tests\test_user_service.py -v

# Test vacation service only
pytest tests\test_vacation_service.py -v
```

## Troubleshooting

### Connection Issues

If `test_connection.py` fails:

1. **Check PostgreSQL is running:**
   ```powershell
   # Windows: Check services
   Get-Service postgresql*
   ```

2. **Verify database exists:**
   ```powershell
   psql -U postgres -l
   ```

3. **Check environment variables:**
   ```powershell
   echo $env:DB_NAME
   echo $env:DB_USER
   ```

4. **Test connection manually:**
   ```powershell
   psql -U postgres -d vacations
   ```

### Common Errors

**Error: "relation does not exist"**
- Solution: Run `schema.sql` to create tables
  ```powershell
  psql -U postgres -d vacations -f sql\schema.sql
  ```

**Error: "password authentication failed"**
- Solution: Check `DB_PASSWORD` environment variable matches your PostgreSQL password

**Error: "database does not exist"**
- Solution: Create the database:
  ```powershell
  createdb -U postgres vacations
  ```

**Error: "could not connect to server"**
- Solution: Ensure PostgreSQL service is running

## Project Structure

```
backend/
├── src/
│   ├── config.py              # Database configuration
│   ├── main.py                # Entry point (runs tests)
│   ├── dal/                   # Data Access Layer
│   │   ├── base_dao.py
│   │   ├── role_dao.py
│   │   ├── user_dao.py
│   │   ├── country_dao.py
│   │   ├── vacation_dao.py
│   │   └── like_dao.py
│   ├── models/
│   │   └── dtos.py
│   └── services/
│       ├── user_service.py
│       └── vacation_service.py
├── sql/
│   └── schema.sql             # Database schema
├── tests/
│   ├── test_db_init.py
│   ├── test_user_service.py
│   ├── test_vacation_service.py
│   └── runner.py
├── test_connection.py         # Connection test script
├── requirements.txt
└── README.md
```

## Notes

- Use a dedicated test database (`test_db`) for running tests
- Tests automatically initialize the database before each run
- All tests use hard-coded values matching seed data
- Passwords are stored in plain text (for learning purposes only)


