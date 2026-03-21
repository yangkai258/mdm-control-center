$body = '{"username":"admin","password":"admin123"}'
try {
    $resp = Invoke-WebRequest -Uri "http://localhost:8085/api/v1/auth/login" -UseBasicParsing -TimeoutSec 5 -Method POST -ContentType 'application/json' -Body $body
    Write-Host "Status: $($resp.StatusCode)"
    Write-Host "Content: $($resp.Content)"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
}
