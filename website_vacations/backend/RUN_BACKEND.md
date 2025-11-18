# How to Run the Backend API Server

## Step-by-Step Instructions

### Step 1: Open Terminal
Open Git Bash, PowerShell, or Command Prompt and navigate to the backend folder:

```bash
cd "E:\Full Stack + Python (John Bryce)\Lessons-uriel\Final Project\website_vacations\backend"
```

### Step 2: Verify Database is Set Up

Make sure PostgreSQL is running and the database exists:

```bash
# Check if database exists (optional)
psql -U postgres -l | grep vacations

# If database doesn't exist, create it:
createdb -U postgres vacations

# Initialize schema (if not done already):
psql -U postgres -d vacations -f sql/schema.sql
```

### Step 3: Check .env File

Make sure you have a `.env` file in the `backend` directory with:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

**Replace `your_postgres_password` with your actual PostgreSQL password!**

### Step 4: Install Dependencies (if not done)

```bash
py -m pip install -r requirements.txt
```

### Step 5: Run the Backend API Server

```bash
py run_api.py
```

You should see:
```
Starting Vacations API server on http://localhost:5000
API endpoints available at http://localhost:5000/api/
 * Running on http://0.0.0.0:5000
```

### Step 6: Test the API

Open a new terminal and test:

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Or open in browser:
# http://localhost:5000/api/health
```

You should see: `{"status":"ok"}`

## Troubleshooting

### Error: "could not connect to server"
- **Solution**: Make sure PostgreSQL service is running
  - Windows: Check Services app, look for "postgresql"
  - Or run: `pg_ctl start` (if PostgreSQL bin is in PATH)

### Error: "password authentication failed"
- **Solution**: Check your `.env` file - `DB_PASSWORD` must match your PostgreSQL password

### Error: "database does not exist"
- **Solution**: Create the database:
  ```bash
  createdb -U postgres vacations
  psql -U postgres -d vacations -f sql/schema.sql
  ```

### Error: "ModuleNotFoundError: No module named 'flask'"
- **Solution**: Install dependencies:
  ```bash
  py -m pip install -r requirements.txt
  ```

### Error: "Address already in use"
- **Solution**: Port 5000 is already in use. Either:
  - Stop the other application using port 5000
  - Or modify `run_api.py` to use a different port

## Quick Commands Summary

```bash
# Navigate to backend
cd backend

# Run the server
py run_api.py
```

**Keep this terminal window open while using the app!**

## What Happens When Backend Runs?

1. ✅ Loads environment variables from `.env`
2. ✅ Connects to PostgreSQL database
3. ✅ Starts Flask API server on port 5000
4. ✅ Enables CORS for frontend communication
5. ✅ API endpoints become available at `http://localhost:5000/api/`

## Next Step

Once the backend is running, open a **NEW terminal** and run the frontend:
```bash
cd frontend
npm run dev
```


