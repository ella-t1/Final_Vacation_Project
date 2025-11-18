# Fix pg_hba.conf and reset password

Write-Host "========================================"
Write-Host "Fix pg_hba.conf and Reset Password"
Write-Host "========================================"
Write-Host ""

$pgHbaPath = "E:\DB\pg_hba.conf"
$backupPath = "$pgHbaPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Check if file exists
if (-not (Test-Path $pgHbaPath)) {
    Write-Host "[ERROR] pg_hba.conf not found at: $pgHbaPath" -ForegroundColor Red
    exit 1
}

Write-Host "Found pg_hba.conf at: $pgHbaPath"
Write-Host "Creating backup: $backupPath"
Copy-Item $pgHbaPath $backupPath

Write-Host ""
Write-Host "Reading current pg_hba.conf..."
$content = Get-Content $pgHbaPath

# Fix and modify authentication
$newContent = @()
$modified = $false

foreach ($line in $content) {
    # Fix lines that might have issues and change md5 to trust temporarily
    if ($line -match "^\s*host\s+all\s+all\s+(127\.0\.0\.1/32|::1/128)\s+\w+") {
        # Replace any auth method with trust
        $newLine = $line -replace '\s+(md5|scram-sha-256|password|trust)', ' trust'
        $newContent += $newLine
        Write-Host "Modified: $line" -ForegroundColor Yellow
        Write-Host "    To:   $newLine" -ForegroundColor Green
        $modified = $true
    } elseif ($line -match "^\s*#") {
        # Keep comments as-is
        $newContent += $line
    } elseif ($line.Trim() -eq "") {
        # Keep empty lines
        $newContent += $line
    } else {
        # Keep other lines as-is
        $newContent += $line
    }
}

if ($modified) {
    Write-Host ""
    Write-Host "Writing modified pg_hba.conf..."
    $newContent | Set-Content $pgHbaPath -Encoding UTF8 -NoNewline:$false
    
    # Ensure file ends with newline
    $finalContent = Get-Content $pgHbaPath -Raw
    if (-not $finalContent.EndsWith("`n")) {
        Add-Content $pgHbaPath -Value ""
    }
    
    Write-Host "[OK] File updated!"
} else {
    Write-Host "[WARNING] No authentication lines found to modify" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================"
Write-Host "Restarting PostgreSQL service..."
Write-Host "========================================"

# Restart service with proper error handling
try {
    $service = Get-Service -Name "postgresql-x64-17" -ErrorAction Stop
    Write-Host "Found service: $($service.DisplayName)"
    
    Write-Host "Stopping service..."
    Stop-Service -Name $service.Name -Force -ErrorAction Stop
    Start-Sleep -Seconds 2
    
    Write-Host "Starting service..."
    Start-Service -Name $service.Name -ErrorAction Stop
    Start-Sleep -Seconds 3
    
    Write-Host "[OK] Service restarted!" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Could not restart service automatically: $_" -ForegroundColor Yellow
    Write-Host "Please restart manually:"
    Write-Host "  Restart-Service postgresql-x64-17"
    Write-Host "  OR use Services app (services.msc)"
}

Write-Host ""
Write-Host "========================================"
Write-Host "Resetting password..."
Write-Host "========================================"

$psqlPath = "C:\Program Files\PostgreSQL\17\bin\psql.exe"
cd "C:\Program Files\PostgreSQL\17\bin"

Write-Host "Connecting to PostgreSQL..."
$output = & $psqlPath -U postgres -c "ALTER USER postgres PASSWORD '123456';" 2>&1

if ($LASTEXITCODE -eq 0 -and $output -notmatch "error" -and $output -notmatch "FATAL") {
    Write-Host "[SUCCESS] Password reset to: 123456" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Password reset failed:" -ForegroundColor Red
    Write-Host $output
    Write-Host ""
    Write-Host "Try connecting manually:"
    Write-Host "  cd `"C:\Program Files\PostgreSQL\17\bin`""
    Write-Host "  .\psql.exe -U postgres"
    Write-Host "  (If it connects, run: ALTER USER postgres PASSWORD '123456';)"
    Write-Host "  \q"
}

Write-Host ""
Write-Host "========================================"
Write-Host "Restoring security (md5)..."
Write-Host "========================================"

# Restore md5 authentication
$restoreContent = @()
foreach ($line in $content) {
    if ($line -match "^\s*host\s+all\s+all\s+(127\.0\.0\.1/32|::1/128)\s+trust") {
        $restoreLine = $line -replace '\s+trust', ' md5'
        $restoreContent += $restoreLine
    } else {
        $restoreContent += $line
    }
}

$restoreContent | Set-Content $pgHbaPath -Encoding UTF8 -NoNewline:$false
Write-Host "[OK] Security restored (md5)"

# Restart service again
try {
    Stop-Service -Name "postgresql-x64-17" -Force -ErrorAction Stop
    Start-Sleep -Seconds 2
    Start-Service -Name "postgresql-x64-17" -ErrorAction Stop
    Start-Sleep -Seconds 3
    Write-Host "[OK] Service restarted with secure authentication" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] Please restart PostgreSQL service manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================"
Write-Host "DONE!"
Write-Host "========================================"
Write-Host ""
Write-Host "Test the connection:"
Write-Host "  cd backend"
Write-Host "  py test_postgres_123456.py"
Write-Host ""
Write-Host "Backup saved at: $backupPath"

