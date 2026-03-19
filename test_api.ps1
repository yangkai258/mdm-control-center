# Test MDM Backend APIs with CORRECT routes
$baseUrl = "http://127.0.0.1:8080"

Write-Host "=== MDM Backend Health Check ===" -ForegroundColor Cyan
Write-Host ""

# 1. Health check
Write-Host "[1] Testing /health endpoint..." -ForegroundColor Yellow
try {
    $r = Invoke-WebRequest -Uri "$baseUrl/health" -TimeoutSec 5
    Write-Host "    Status: $($r.StatusCode)" -ForegroundColor Green
    Write-Host "    Response: $($r.Content)"
} catch {
    Write-Host "    ERROR: Unable to connect" -ForegroundColor Red
}

Write-Host ""

# 2. Device list (correct path: /api/v1/devices)
Write-Host "[2] Testing GET /api/v1/devices..." -ForegroundColor Yellow
try {
    $r = Invoke-WebRequest -Uri "$baseUrl/api/v1/devices" -TimeoutSec 5
    Write-Host "    Status: $($r.StatusCode)" -ForegroundColor Green
    Write-Host "    Response: $($r.Content)"
} catch {
    $stream = $_.Exception.Response.GetResponseStream()
    $reader = [System.IO.StreamReader]::new($stream)
    $body = $reader.ReadToEnd()
    $reader.Close()
    Write-Host "    Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
    Write-Host "    Response: $body"
}

Write-Host ""

# 3. Device register
Write-Host "[3] Testing POST /api/v1/devices/register..." -ForegroundColor Yellow
try {
    $body = '{"mac_address":"AA:BB:CC:DD:EE:FF","sn_code":"SN123456","hardware_model":"M5_CoreS3","firmware_version":"1.0.0"}'
    $r = Invoke-WebRequest -Uri "$baseUrl/api/v1/devices/register" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 5
    Write-Host "    Status: $($r.StatusCode)" -ForegroundColor Green
    Write-Host "    Response: $($r.Content)"
} catch {
    $stream = $_.Exception.Response.GetResponseStream()
    $reader = [System.IO.StreamReader]::new($stream)
    $respBody = $reader.ReadToEnd()
    $reader.Close()
    Write-Host "    Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
    Write-Host "    Response: $respBody"
}

Write-Host ""

# 4. Non-existent device
Write-Host "[4] Testing GET /api/v1/devices/nonexistent-id..." -ForegroundColor Yellow
try {
    $r = Invoke-WebRequest -Uri "$baseUrl/api/v1/devices/nonexistent-id" -TimeoutSec 5
    Write-Host "    Status: $($r.StatusCode)" -ForegroundColor Green
} catch {
    $stream = $_.Exception.Response.GetResponseStream()
    $reader = [System.IO.StreamReader]::new($stream)
    $respBody = $reader.ReadToEnd()
    $reader.Close()
    Write-Host "    Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Green
    Write-Host "    Response: $respBody"
}

Write-Host ""
Write-Host "=== Backend Test Complete ===" -ForegroundColor Cyan
