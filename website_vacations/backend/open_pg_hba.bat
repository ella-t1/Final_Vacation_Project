@echo off
echo Opening pg_hba.conf in Notepad...
echo Location: E:\DB\pg_hba.conf
echo.
start notepad "E:\DB\pg_hba.conf"
echo.
echo File should open in Notepad.
echo.
echo INSTRUCTIONS:
echo 1. Find these lines (around line 90-95):
echo    host    all             all             127.0.0.1/32            scram-sha-256
echo    host    all             all             ::1/128                 scram-sha-256
echo.
echo 2. Change "scram-sha-256" to "trust" temporarily:
echo    host    all             all             127.0.0.1/32            trust
echo    host    all             all             ::1/128                 trust
echo.
echo 3. Save the file (Ctrl+S)
echo.
echo 4. Restart PostgreSQL service
echo.
echo 5. Reset password (see next steps)
echo.
pause

