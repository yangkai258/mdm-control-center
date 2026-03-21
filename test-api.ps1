# Check what port MDM backend is actually on
$body = '{"username":"admin","password":"admin123"}'

# Try port 8082 (found in netstat)
try {
    $resp = Invoke-WebRequest -Uri "http://localhost:8082/api/v1/auth/login" -UseBasicParsing -TimeoutSec 3 -Method POST -ContentType 'application/json' -Body $body
    Write-Host "8082: Status=$($resp.StatusCode) Content=$($resp.Content)"
} catch {
    Write-Host "8082: ERROR - $($_.Exception.Message)"
}

# Try port 8080 directly (bypass OpenClaw gateway?)
try {
    $resp = Invoke-WebRequest -Uri "http://127.0.0.1:8080/api/v1/devices" -UseBasicParsing -TimeoutSec 3 -Headers @{'Origin'='http://localhost:3000'}
    Write-Host "8080 direct: Status=$($resp.StatusCode)"
} catch {
    Write-Host "8080 direct: ERROR - $($_.Exception.Message)"
}
