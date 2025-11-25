@echo off
REM Simple database setup script
REM Usage: setup_database.bat your_postgres_password

echo ============================================================
echo PostgreSQL Database Setup
echo ============================================================
echo.

if "%1"=="" (
    echo ERROR: Please provide your PostgreSQL password as an argument
    echo Usage: setup_database.bat your_postgres_password
    echo.
    echo Or set it as environment variable:
    echo   set DB_PASSWORD=your_password
    echo   setup_database.bat
    exit /b 1
)

set DB_PASSWORD=%1
py setup_database.py %1

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Creating .env file...
    (
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo DB_NAME=vacations
        echo DB_USER=postgres
        echo DB_PASSWORD=%1
    ) > .env
    echo.
    echo Setup complete! You can now run: py src\main.py
) else (
    echo.
    echo Setup failed. Please check the errors above.
    exit /b 1
)

