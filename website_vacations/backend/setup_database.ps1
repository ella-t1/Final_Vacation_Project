# PowerShell script to set up PostgreSQL database for Vacations project
# Run this script from the backend directory

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Database Setup Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Prompt for PostgreSQL password
$password = Read-Host "Enter your PostgreSQL admin password (postgres user)" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

if ([string]::IsNullOrWhiteSpace($plainPassword)) {
    Write-Host "ERROR: Password cannot be empty!" -ForegroundColor Red
    exit 1
}

# Set environment variable
$env:DB_PASSWORD = $plainPassword

Write-Host ""
Write-Host "Running database setup script..." -ForegroundColor Yellow
Write-Host ""

# Run the Python setup script
py setup_database.py

# Check if setup was successful
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    
    # Create .env file
    $envContent = @"
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vacations
DB_USER=postgres
DB_PASSWORD=$plainPassword
"@
    
    $envFile = Join-Path $PSScriptRoot ".env"
    $envContent | Out-File -FilePath $envFile -Encoding utf8 -NoNewline
    
    Write-Host "✓ Created .env file at: $envFile" -ForegroundColor Green
    Write-Host ""
    Write-Host "Setup complete! You can now run:" -ForegroundColor Green
    Write-Host "  py src/main.py" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "Setup failed. Please check the errors above." -ForegroundColor Red
    exit 1
}

