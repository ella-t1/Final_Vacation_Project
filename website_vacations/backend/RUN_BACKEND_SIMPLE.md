# How to Run the Backend

## Quick Start

### Step 1: Navigate to Backend Directory

```powershell
cd "E:\Full Stack + Python (John Bryce)\Lessons-uriel\Final Project\website_vacations\backend"
```

### Step 2: Run the API Server

```powershell
py run_api.py
```

### Step 3: Verify It's Running

You should see:
```
Starting Vacations API server on http://localhost:5000
API endpoints available at http://localhost:5000/api/
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 4: Test the API

Open in browser: http://localhost:5000/api/health

Or in terminal:
```powershell
curl http://localhost:5000/api/health
```

You should see: `{"status":"ok"}`

## Keep It Running

**Important:** Keep the terminal window open while using the app!

The backend must be running for the frontend to work.

## Stop the Server

Press `Ctrl + C` in the terminal where it's running.

## Troubleshooting

### Port 5000 Already in Use
- Stop the other application using port 5000
- Or change port in `run_api.py`: `app.run(debug=True, host="0.0.0.0", port=5001)`

### Database Connection Error
- Make sure PostgreSQL service is running
- Check `.env` file has correct settings
- Verify database 'vacations' exists

### Module Not Found
- Install dependencies: `py -m pip install -r requirements.txt`

## API Endpoints

Once running, these endpoints are available:

- `GET http://localhost:5000/api/health` - Health check
- `POST http://localhost:5000/api/users/register` - Register user
- `POST http://localhost:5000/api/users/login` - Login
- `GET http://localhost:5000/api/vacations` - List vacations
- `GET http://localhost:5000/api/countries` - List countries
- `POST http://localhost:5000/api/vacations` - Create vacation (Admin)
- `PUT http://localhost:5000/api/vacations/<id>` - Update vacation (Admin)
- `DELETE http://localhost:5000/api/vacations/<id>` - Delete vacation (Admin)
- `POST http://localhost:5000/api/users/<user_id>/likes/<vacation_id>` - Like vacation
- `DELETE http://localhost:5000/api/users/<user_id>/likes/<vacation_id>` - Unlike vacation

