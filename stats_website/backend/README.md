# Statistics Website Backend

Backend API for the statistics website (Part III of the project).

## Overview

This backend connects to the **same PostgreSQL database** used in Part II (vacations website). It provides statistics endpoints accessible only to Admin users.

## Database Connection

The backend connects to PostgreSQL using the same database from Part II:
- **Database Name**: `vacations` (same as Part II)
- **Connection**: Uses `psycopg2` library
- **Configuration**: Environment variables or defaults

### Connection Configuration

The connection is configured in `src/config.py`:
- Reads from environment variables
- Defaults to: `localhost:5432`, database `vacations`, user `postgres`, password `postgres`

### Environment Variables

Create a `.env` file (optional):
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=postgres
FLASK_PORT=5001
FLASK_DEBUG=True
```

## Setup

### 1. Install Dependencies

```bash
# Using py command (Windows)
py -m pip install -r requirements.txt

# Or with virtual environment
py -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Test Database Connection

```bash
py test_db_connection.py
```

This will:
- Test PostgreSQL connection
- Show database version
- List all tables
- Verify required tables exist
- Check for admin user

### 3. Test Imports

```bash
py test_backend.py
```

### 4. Run the Server

```bash
py run_api.py
```

Server will start on `http://localhost:5001`

## API Endpoints

### Public
- `GET /health` - Health check

### Authentication
- `POST /login` - Admin login (username/email + password)
- `POST /logout` - Logout

### Statistics (Admin Only)
- `GET /vacations/stats` - Vacation statistics (past/ongoing/future)
- `GET /users/total` - Total users count
- `GET /likes/total` - Total likes count
- `GET /likes/distribution` - Likes distribution by destination

## Testing

See `test_setup.md` for detailed testing instructions.

Quick test:
```bash
# Health check
curl http://localhost:5001/health

# Login
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin1234"}' \
  -c cookies.txt

# Get stats
curl http://localhost:5001/vacations/stats -b cookies.txt
```

## Project Structure

```
backend/
├── src/
│   ├── config.py              # Database configuration
│   ├── main.py                # Entry point
│   ├── dal/                   # Data Access Layer
│   │   ├── base_dao.py
│   │   ├── user_dao.py
│   │   ├── vacation_dao.py
│   │   ├── like_dao.py
│   │   └── role_dao.py
│   ├── services/              # Business Logic Layer
│   │   ├── auth_service.py
│   │   └── statistics_service.py
│   └── api/                   # API Layer
│       ├── app.py
│       └── routes.py
├── requirements.txt
├── run_api.py                 # Run script
├── test_backend.py            # Test imports
└── test_db_connection.py      # Test database connection
```

## Important Notes

1. **Same Database**: This backend uses the **same PostgreSQL database** as Part II
2. **No Schema Changes**: The database schema is not modified - we only read data
3. **Admin Only**: All statistics endpoints require Admin authentication
4. **Session Based**: Authentication uses Flask sessions (cookies)

