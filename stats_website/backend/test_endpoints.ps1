# PowerShell test script for backend API endpoints
# Make sure the server is running on http://localhost:5001

$BaseUrl = "http://localhost:5001"
$CookieFile = "cookies.txt"

Write-Host "=== Testing Statistics Backend API ===" -ForegroundColor Cyan
Write-Host ""

# Test 1: Health Check
Write-Host "1. Testing Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
    $response | ConvertTo-Json
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: Login (should succeed for admin)
Write-Host "2. Testing Login (Admin)..." -ForegroundColor Yellow
try {
    $loginBody = @{
        username = "admin"
        password = "admin1234"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$BaseUrl/login" -Method Post `
        -Body $loginBody -ContentType "application/json" `
        -SessionVariable session
    
    Write-Host "Login successful!" -ForegroundColor Green
    $response | ConvertTo-Json
    
    # Test 3: Get Statistics (with auth)
    Write-Host ""
    Write-Host "3. Testing Vacation Statistics..." -ForegroundColor Yellow
    $stats = Invoke-RestMethod -Uri "$BaseUrl/vacations/stats" -WebSession $session
    $stats | ConvertTo-Json
    
    Write-Host ""
    Write-Host "4. Testing Total Users..." -ForegroundColor Yellow
    $users = Invoke-RestMethod -Uri "$BaseUrl/users/total" -WebSession $session
    $users | ConvertTo-Json
    
    Write-Host ""
    Write-Host "5. Testing Total Likes..." -ForegroundColor Yellow
    $likes = Invoke-RestMethod -Uri "$BaseUrl/likes/total" -WebSession $session
    $likes | ConvertTo-Json
    
    Write-Host ""
    Write-Host "6. Testing Likes Distribution..." -ForegroundColor Yellow
    $distribution = Invoke-RestMethod -Uri "$BaseUrl/likes/distribution" -WebSession $session
    $distribution | ConvertTo-Json
    
    Write-Host ""
    Write-Host "7. Testing Logout..." -ForegroundColor Yellow
    $logout = Invoke-RestMethod -Uri "$BaseUrl/logout" -Method Post -WebSession $session
    $logout | ConvertTo-Json
    
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    if ($_.Exception.Response.StatusCode -eq 403) {
        Write-Host "Admin access required - check database for admin user" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "=== Testing Complete ===" -ForegroundColor Cyan

