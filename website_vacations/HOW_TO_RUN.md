# How to Run the Vacations Project

This guide will help you run both the backend API server and the frontend React application.

## Prerequisites

1. **PostgreSQL** - Make sure PostgreSQL is installed and running
2. **Python 3.x** - Already installed (Python 3.13.0)
3. **Node.js** - Required for the frontend

## Step 1: Database Setup

### 1.1 Create the Database

```bash
# Create main database
createdb -U postgres vacations

# Or using psql:
psql -U postgres -c "CREATE DATABASE vacations;"
```

### 1.2 Initialize Database Schema

```bash
cd backend
psql -U postgres -d vacations -f sql/schema.sql
```

This will create all tables and insert seed data (users, countries, vacations).

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Install Python Dependencies

**On Windows (Git Bash or PowerShell):**
```bash
py -m pip install -r requirements.txt
```

**On Linux/Mac:**
```bash
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

### 2.3 Set Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# backend/.env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here
```

**Or set them temporarily in PowerShell:**
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="5432"
$env:DB_NAME="vacations"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
```

### 2.4 Run the Backend API Server

```bash
# Windows
py run_api.py

# Linux/Mac
python run_api.py
```

The API server will start on **http://localhost:5000**

You should see:
```
Starting Vacations API server on http://localhost:5000
API endpoints available at http://localhost:5000/api/
```

**Keep this terminal window open!**

## Step 3: Frontend Setup

### 3.1 Open a New Terminal Window

Keep the backend running and open a **new terminal**.

### 3.2 Navigate to Frontend Directory

```bash
cd frontend
```

### 3.3 Install Node Dependencies

```bash
npm install
```

This only needs to be done once (or when dependencies change).

### 3.4 Run the Frontend Development Server

```bash
npm run dev
```

The frontend will start on **http://localhost:5173**

You should see:
```
VITE v7.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

## Step 4: Access the Application

1. Open your browser and go to: **http://localhost:5173**
2. You should see the Vacations homepage

## Default Login Credentials

After running the database schema, you'll have these users:

**Admin User:**
- Email: `admin@vacations.com`
- Password: `admin1234`

**Regular User:**
- Email: `john@example.com`
- Password: `user1234`

## Quick Start Commands Summary

### Terminal 1 - Backend:
```bash
cd backend
py run_api.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## Troubleshooting

### Backend Issues

**Error: "could not connect to server"**
- Make sure PostgreSQL is running
- Check your DB_HOST and DB_PORT in .env

**Error: "password authentication failed"**
- Verify your DB_PASSWORD in .env matches your PostgreSQL password

**Error: "database does not exist"**
- Run: `createdb -U postgres vacations`
- Then run: `psql -U postgres -d vacations -f sql/schema.sql`

### Frontend Issues

**Error: "Cannot connect to API"**
- Make sure the backend is running on port 5000
- Check that CORS is enabled in the backend

**Port 5173 already in use**
- The frontend will automatically use the next available port
- Or stop the process using port 5173

## Project Structure

```
website_vacations/
├── backend/          # Python Flask API
│   ├── src/
│   │   ├── api/     # API routes and app
│   │   ├── dal/     # Data Access Layer
│   │   ├── models/  # DTOs
│   │   └── services/# Business Logic
│   ├── sql/         # Database schema
│   └── run_api.py   # API server entry point
│
└── frontend/        # React TypeScript app
    ├── src/
    │   ├── pages/   # Page components
    │   ├── components/
    │   ├── store/   # Redux store
    │   └── utils/   # API utilities
    └── package.json
```

## API Endpoints

Once the backend is running, you can access:

- `GET http://localhost:5000/api/health` - Health check
- `POST http://localhost:5000/api/users/register` - Register user
- `POST http://localhost:5000/api/users/login` - Login
- `GET http://localhost:5000/api/vacations` - List vacations
- `GET http://localhost:5000/api/countries` - List countries
- And more...

## Next Steps

1. ✅ Backend running on port 5000
2. ✅ Frontend running on port 5173
3. ✅ Database initialized with seed data
4. 🎉 Open http://localhost:5173 and start using the app!


