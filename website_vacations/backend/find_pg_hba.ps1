# Script to find pg_hba.conf location

Write-Host "========================================"
Write-Host "Finding PostgreSQL pg_hba.conf"
Write-Host "========================================"
Write-Host ""

# Method 1: Try to query PostgreSQL directly
Write-Host "Method 1: Querying PostgreSQL for data directory..."
$psqlPath = "C:\Program Files\PostgreSQL\17\bin\psql.exe"

if (Test-Path $psqlPath) {
    try {
        # Try to get data directory (might fail if password required)
        $dataDir = & $psqlPath -U postgres -t -c "SHOW data_directory;" 2>&1 | Where-Object { $_ -notmatch "password" -and $_ -notmatch "error" -and $_.Trim() -ne "" }
        if ($dataDir -and (Test-Path $dataDir.Trim())) {
            $pgHbaPath = Join-Path $dataDir.Trim() "pg_hba.conf"
            if (Test-Path $pgHbaPath) {
                Write-Host "[FOUND] pg_hba.conf at: $pgHbaPath" -ForegroundColor Green
                Write-Host ""
                Write-Host "To reset password manually:"
                Write-Host "1. Open as Administrator: notepad `"$pgHbaPath`""
                Write-Host "2. Find lines with 'md5' and change to 'trust' temporarily"
                Write-Host "3. Restart PostgreSQL service"
                Write-Host "4. Run: cd `"C:\Program Files\PostgreSQL\17\bin`""
                Write-Host "5. Run: .\psql.exe -U postgres -c `"ALTER USER postgres PASSWORD '123456';`""
                Write-Host "6. Change 'trust' back to 'md5' in pg_hba.conf"
                Write-Host "7. Restart PostgreSQL service again"
                exit 0
            }
        }
    } catch {
        Write-Host "Could not query PostgreSQL (password required)" -ForegroundColor Yellow
    }
}

# Method 2: Search common locations
Write-Host ""
Write-Host "Method 2: Searching common locations..."

$searchPaths = @(
    "C:\Program Files\PostgreSQL\17\data",
    "C:\ProgramData\PostgreSQL\17",
    "E:\DB",
    "C:\PostgreSQL\17\data"
)

foreach ($path in $searchPaths) {
    if (Test-Path $path) {
        Write-Host "Checking: $path"
        $pgHba = Join-Path $path "pg_hba.conf"
        if (Test-Path $pgHba) {
            Write-Host "[FOUND] pg_hba.conf at: $pgHba" -ForegroundColor Green
            Write-Host ""
            Write-Host "To reset password:"
            Write-Host "1. Open as Administrator: notepad `"$pgHba`""
            Write-Host "2. Find and change 'md5' to 'trust' for localhost connections"
            Write-Host "3. Restart PostgreSQL: Restart-Service postgresql-x64-17"
            Write-Host "4. Reset password: cd `"C:\Program Files\PostgreSQL\17\bin`" ^&^& .\psql.exe -U postgres -c `"ALTER USER postgres PASSWORD '123456';`""
            Write-Host "5. Change 'trust' back to 'md5'"
            Write-Host "6. Restart PostgreSQL again"
            exit 0
        }
    }
}

# Method 3: Search entire drive (slower)
Write-Host ""
Write-Host "Method 3: Searching for pg_hba.conf (this may take a moment)..."
$found = Get-ChildItem "C:\" -Recurse -Filter "pg_hba.conf" -ErrorAction SilentlyContinue -Depth 4 | Select-Object -First 1

if ($found) {
    Write-Host "[FOUND] pg_hba.conf at: $($found.FullName)" -ForegroundColor Green
} else {
    Write-Host "[NOT FOUND] Could not locate pg_hba.conf automatically" -ForegroundColor Red
    Write-Host ""
    Write-Host "ALTERNATIVE METHOD: Reset password via pgAdmin"
    Write-Host "1. Open pgAdmin"
    Write-Host "2. Connect to PostgreSQL server"
    Write-Host "3. Right-click 'postgres' user → Properties → Definition"
    Write-Host "4. Set password to '123456'"
    Write-Host "5. Save"
}

