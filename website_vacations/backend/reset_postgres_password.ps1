# PostgreSQL Password Reset Script
# This script attempts to reset the PostgreSQL password to '123456'

Write-Host "========================================"
Write-Host "PostgreSQL Password Reset Helper"
Write-Host "========================================"
Write-Host ""

# Find PostgreSQL installation
$pgPaths = @(
    "C:\Program Files\PostgreSQL\17\bin",
    "C:\Program Files\PostgreSQL\16\bin",
    "C:\Program Files\PostgreSQL\15\bin",
    "C:\Program Files\PostgreSQL\14\bin",
    "C:\Program Files\PostgreSQL\13\bin"
)

$psqlPath = $null
foreach ($path in $pgPaths) {
    if (Test-Path "$path\psql.exe") {
        $psqlPath = $path
        Write-Host "Found PostgreSQL at: $psqlPath"
        break
    }
}

if (-not $psqlPath) {
    Write-Host "[ERROR] PostgreSQL not found in common locations." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please find psql.exe manually:"
    Write-Host "1. Look in: C:\Program Files\PostgreSQL\"
    Write-Host "2. Find your version folder (e.g., 15, 16, 17)"
    Write-Host "3. Navigate to: bin\psql.exe"
    Write-Host ""
    Write-Host "Then run manually:"
    Write-Host "  cd 'path\to\postgresql\bin'"
    Write-Host "  .\psql.exe -U postgres"
    Write-Host "  ALTER USER postgres PASSWORD '123456';"
    Write-Host "  \q"
    exit 1
}

Write-Host ""
Write-Host "Attempting to reset password to: 123456"
Write-Host "You may be prompted for the current password."
Write-Host "If you don't know it, try pressing Enter (empty password)."
Write-Host ""

cd $psqlPath
.\psql.exe -U postgres -c "ALTER USER postgres PASSWORD '123456';"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "SUCCESS! Password has been reset to: 123456" -ForegroundColor Green
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "1. Make sure backend/.env file contains: DB_PASSWORD=123456"
    Write-Host "2. Test the connection:"
    Write-Host "   cd backend"
    Write-Host "   py test_postgres_123456.py"
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "FAILED to reset password automatically." -ForegroundColor Red
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Try these alternatives:"
    Write-Host ""
    Write-Host "Option 1: Connect manually"
    Write-Host "  cd `"$psqlPath`""
    Write-Host "  .\psql.exe -U postgres"
    Write-Host "  ALTER USER postgres PASSWORD '123456';"
    Write-Host "  \q"
    Write-Host ""
    Write-Host "Option 2: Use pgAdmin"
    Write-Host "  - Open pgAdmin"
    Write-Host "  - Connect to server"
    Write-Host "  - Right-click 'postgres' user → Properties"
    Write-Host "  - Set password to '123456'"
    Write-Host ""
    Write-Host "Option 3: Temporarily allow passwordless connection"
    Write-Host "  See RESET_POSTGRES_PASSWORD_GUIDE.md for details"
    Write-Host ""
}

