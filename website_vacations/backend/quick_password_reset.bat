@echo off
echo ========================================
echo PostgreSQL Password Reset Helper
echo ========================================
echo.

echo This script will help you reset the PostgreSQL password.
echo.

echo Step 1: Finding PostgreSQL installation...
echo.

REM Try common PostgreSQL installation paths
set PG_PATH=
if exist "C:\Program Files\PostgreSQL\16\bin\psql.exe" (
    set PG_PATH=C:\Program Files\PostgreSQL\16\bin
    echo Found PostgreSQL 16 at: %PG_PATH%
) else if exist "C:\Program Files\PostgreSQL\15\bin\psql.exe" (
    set PG_PATH=C:\Program Files\PostgreSQL\15\bin
    echo Found PostgreSQL 15 at: %PG_PATH%
) else if exist "C:\Program Files\PostgreSQL\14\bin\psql.exe" (
    set PG_PATH=C:\Program Files\PostgreSQL\14\bin
    echo Found PostgreSQL 14 at: %PG_PATH%
) else if exist "C:\Program Files\PostgreSQL\13\bin\psql.exe" (
    set PG_PATH=C:\Program Files\PostgreSQL\13\bin
    echo Found PostgreSQL 13 at: %PG_PATH%
) else (
    echo PostgreSQL not found in common locations.
    echo Please find your PostgreSQL installation manually.
    echo Usually: C:\Program Files\PostgreSQL\VERSION\bin
    pause
    exit /b 1
)

echo.
echo Step 2: Attempting to connect to PostgreSQL...
echo.
echo You will be prompted for the current password.
echo If you don't know it, try pressing Enter (empty password).
echo.

cd /d "%PG_PATH%"
psql -U postgres -c "ALTER USER postgres PASSWORD '123456';"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Password has been reset to: 123456
    echo ========================================
    echo.
    echo Your backend/.env file should now work with:
    echo DB_PASSWORD=123456
    echo.
) else (
    echo.
    echo ========================================
    echo FAILED to reset password automatically.
    echo ========================================
    echo.
    echo Please try manually:
    echo 1. Open Command Prompt as Administrator
    echo 2. cd "%PG_PATH%"
    echo 3. psql -U postgres
    echo 4. Then run: ALTER USER postgres PASSWORD '123456';
    echo 5. Type: \q to exit
    echo.
)

pause

