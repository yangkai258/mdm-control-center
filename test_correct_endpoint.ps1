$ErrorActionPreference = "Continue"
$baseUrl = "http://localhost:8080"

# Login first and get token
Write-Host "=== 1. Login ===" -ForegroundColor Cyan
$body = '{"username":"admin","password":"admin123"}'
$wr = [System.Net.WebRequest]::CreateHttp("$baseUrl/api/v1/auth/login")
$wr.Method = "POST"; $wr.ContentType = "application/json"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
$wr.ContentLength = $bytes.Length
$reqStream = $wr.GetRequestStream(); $reqStream.Write($bytes,0,$bytes.Length); $reqStream.Close()
$resp = $wr.GetResponse()
$reader = [System.IO.StreamReader]::new($resp.GetResponseStream())
$content = $reader.ReadToEnd(); $reader.Close(); $resp.Close()
$token = ($content | ConvertFrom-Json).data.token

# Test departments using CORRECT endpoint per documentation
Write-Host "`n=== 2. Department Tests (using /api/v1/org prefix) ===" -ForegroundColor Cyan
$headers = @{"Authorization"="Bearer $token"}

# GET /api/v1/org/departments
try {
    $wr = [System.Net.WebRequest]::CreateHttp("$baseUrl/api/v1/org/departments")
    $wr.Method = "GET"; $headers.GetEnumerator() | ForEach-Object { $wr.Headers[$_.Key] = $_.Value }
    $resp = $wr.GetResponse()
    $reader = [System.IO.StreamReader]::new($resp.GetResponseStream())
    $content = $reader.ReadToEnd(); $reader.Close(); $resp.Close()
    Write-Host "[PASS] GET /api/v1/org/departments | HTTP $([int]$resp.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] GET /api/v1/org/departments | $($_.Exception.Message)" -ForegroundColor Red
}

# POST /api/v1/org/departments
$body = '{"dept_name":"测试部门","dept_code":"TEST001"}'
try {
    $wr = [System.Net.WebRequest]::CreateHttp("$baseUrl/api/v1/org/departments")
    $wr.Method = "POST"; $wr.ContentType = "application/json"
    $headers.GetEnumerator() | ForEach-Object { $wr.Headers[$_.Key] = $_.Value }
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    $wr.ContentLength = $bytes.Length
    $reqStream = $wr.GetRequestStream(); $reqStream.Write($bytes,0,$bytes.Length); $reqStream.Close()
    $resp = $wr.GetResponse()
    $reader = [System.IO.StreamReader]::new($resp.GetResponseStream())
    $content = $reader.ReadToEnd(); $reader.Close(); $resp.Close()
    Write-Host "[PASS] POST /api/v1/org/departments | HTTP $([int]$resp.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "[FAIL] POST /api/v1/org/departments | $($_.Exception.Message)" -ForegroundColor Red
}