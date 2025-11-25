# PowerShell script to reset PostgreSQL password by temporarily modifying pg_hba.conf

Write-Host "========================================"
Write-Host "PostgreSQL Password Reset via pg_hba.conf"
Write-Host "========================================"
Write-Host ""

# Find pg_hba.conf - PostgreSQL data directory is at E:\DB
$pgHbaPath = "E:\DB\pg_hba.conf"

if (-not (Test-Path $pgHbaPath)) {
    Write-Host "[ERROR] pg_hba.conf not found at: $pgHbaPath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying to find it..."
    # Try alternative locations
    $alternatives = @(
        "C:\Program Files\PostgreSQL\17\data\pg_hba.conf",
        "C:\ProgramData\PostgreSQL\17\pg_hba.conf"
    )
    
    $found = $false
    foreach ($alt in $alternatives) {
        if (Test-Path $alt) {
            $pgHbaPath = $alt
            Write-Host "Found at: $pgHbaPath" -ForegroundColor Green
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        # Search for it
        $searchResult = Get-ChildItem "C:\" -Recurse -Filter "pg_hba.conf" -ErrorAction SilentlyContinue -Depth 4 | Select-Object -First 1
        if ($searchResult) {
            $pgHbaPath = $searchResult.FullName
            Write-Host "Found at: $pgHbaPath" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Could not find pg_hba.conf" -ForegroundColor Red
            Write-Host "PostgreSQL data directory should be at: E:\DB"
            Write-Host "Please check if pg_hba.conf exists there."
            exit 1
        }
    }
}

Write-Host "Found pg_hba.conf at: $pgHbaPath"
Write-Host ""

# Backup original file
$backupPath = "$pgHbaPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "Creating backup: $backupPath"
Copy-Item $pgHbaPath $backupPath

Write-Host ""
Write-Host "Reading pg_hba.conf..."
$content = Get-Content $pgHbaPath

# Find and replace authentication methods
$modified = $false
$newContent = @()

foreach ($line in $content) {
    if ($line -match "^\s*host\s+all\s+all\s+(127\.0\.0\.1/32|::1/128)\s+\w+") {
        # Replace md5/scram-sha-256 with trust temporarily
        $newLine = $line -replace '\s+(md5|scram-sha-256|password)', ' trust'
        $newContent += $newLine
        Write-Host "Modified: $line" -ForegroundColor Yellow
        Write-Host "    To:   $newLine" -ForegroundColor Green
        $modified = $true
    } else {
        $newContent += $line
    }
}

if (-not $modified) {
    Write-Host "[WARNING] No authentication lines found to modify." -ForegroundColor Yellow
    Write-Host "The file might already be configured differently."
    Write-Host ""
    Write-Host "Current relevant lines:"
    $content | Select-String "host.*all.*all" | ForEach-Object { Write-Host "  $_" }
    Write-Host ""
    Write-Host "Please check the file manually and ensure these lines use 'trust':"
    Write-Host "  host    all    all    127.0.0.1/32    trust"
    Write-Host "  host    all    all    ::1/128         trust"
} else {
    # Write modified content
    Write-Host ""
    Write-Host "Writing modified pg_hba.conf..."
    $newContent | Set-Content $pgHbaPath -Encoding UTF8
    
    Write-Host "[OK] pg_hba.conf modified successfully!"
}

Write-Host ""
Write-Host "========================================"
Write-Host "Restarting PostgreSQL service..."
Write-Host "========================================"

# Find and restart PostgreSQL service
$services = Get-Service | Where-Object { $_.Name -like "*postgresql*" -or $_.DisplayName -like "*PostgreSQL*" }
if ($services) {
    $service = $services | Select-Object -First 1
    Write-Host "Found service: $($service.DisplayName)"
    Write-Host "Restarting..."
    Restart-Service -Name $service.Name -Force
    Start-Sleep -Seconds 3
    Write-Host "[OK] Service restarted!"
} else {
    Write-Host "[WARNING] Could not find PostgreSQL service automatically." -ForegroundColor Yellow
    Write-Host "Please restart it manually:"
    Write-Host "  Restart-Service postgresql-x64-17"
    Write-Host "  OR use Services app (services.msc)"
}

Write-Host ""
Write-Host "========================================"
Write-Host "Now resetting password..."
Write-Host "========================================"
Write-Host ""

# Now try to connect and reset password
$psqlPath = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
cd "C:\Program Files\PostgreSQL\17\bin"

Write-Host "Connecting to PostgreSQL (should work without password now)..."
$result = & $psqlPath -U postgres -c "ALTER USER postgres PASSWORD '123456';" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "[SUCCESS] Password reset to: 123456" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to reset password:" -ForegroundColor Red
    Write-Host $result
    Write-Host ""
    Write-Host "Try manually:"
    Write-Host "  cd `"C:\Program Files\PostgreSQL\17\bin`""
    Write-Host "  .\psql.exe -U postgres"
    Write-Host "  ALTER USER postgres PASSWORD '123456';"
    Write-Host "  \q"
}

Write-Host ""
Write-Host "========================================"
Write-Host "Restoring security (changing back to md5)..."
Write-Host "========================================"

# Restore original authentication
$restoreContent = @()
foreach ($line in $content) {
    if ($line -match "^\s*host\s+all\s+all\s+(127\.0\.0\.1/32|::1/128)\s+trust") {
        # Change trust back to md5
        $restoreLine = $line -replace '\s+trust', ' md5'
        $restoreContent += $restoreLine
        Write-Host "Restored: $restoreLine" -ForegroundColor Green
    } else {
        $restoreContent += $line
    }
}

$restoreContent | Set-Content $pgHbaPath -Encoding UTF8
Write-Host "[OK] Security restored (md5 authentication)"

# Restart service again
if ($services) {
    Restart-Service -Name $service.Name -Force
    Write-Host "[OK] Service restarted with secure authentication"
}

Write-Host ""
Write-Host "========================================"
Write-Host "DONE!"
Write-Host "========================================"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Test connection: cd backend ^&^& py test_postgres_123456.py"
Write-Host "2. Make sure backend/.env has: DB_PASSWORD=123456"
Write-Host ""
Write-Host "Backup saved at: $backupPath"

