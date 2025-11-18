@echo off
echo ========================================
echo PostgreSQL Password Reset
echo ========================================
echo.
echo This will reset the PostgreSQL password to: 123456
echo.
pause

cd "C:\Program Files\PostgreSQL\17\bin"

echo.
echo Attempting to connect to PostgreSQL...
echo If prompted for password, try pressing Enter (empty password)
echo.

psql.exe -U postgres -c "ALTER USER postgres PASSWORD '123456';"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Password reset to: 123456
    echo ========================================
    echo.
    echo Next steps:
    echo 1. Make sure backend/.env has: DB_PASSWORD=123456
    echo 2. Test connection: cd backend ^&^& py test_postgres_123456.py
    echo.
) else (
    echo.
    echo ========================================
    echo FAILED - Could not reset password automatically
    echo ========================================
    echo.
    echo Try this manually:
    echo 1. Open Command Prompt as Administrator
    echo 2. cd "C:\Program Files\PostgreSQL\17\bin"
    echo 3. psql.exe -U postgres
    echo 4. ALTER USER postgres PASSWORD '123456';
    echo 5. \q
    echo.
)

pause

