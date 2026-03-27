$ErrorActionPreference = "Continue"
$baseUrl = "http://localhost:8080"

function Test-API {
    param([string]$Name, [string]$Method, [string]$Endpoint, [string]$Body = "", [bool]$Auth = $true)
    $url = "$baseUrl$Endpoint"
    $headers = @{"Content-Type" = "application/json"}
    if ($Auth -and $global:token) {
        $headers["Authorization"] = "Bearer $global:token"
    }
    
    try {
        $params = @{Uri = $url; Method = $Method; Headers = $headers}
        if ($Body) { $params["Body"] = $Body }
        $resp = Invoke-WebRequest @params -ErrorAction Stop
        $status = $resp.StatusCode
        $content = $resp.Content | ConvertFrom-Json
        Write-Host "[PASS] $Name - HTTP $status" -ForegroundColor Green
        if ($content) { 
            $json = $content | ConvertTo-Json -Depth 5
            Write-Host "       Response: $($json.Substring(0, [Math]::Min(200, $json.Length)))"
        }
        return @{success=$true; status=$status; data=$content}
    } catch {
        $ex = $_.Exception
        if ($ex.Response) {
            $status = [int]$ex.Response.StatusCode
            $stream = $ex.Response.GetResponseStream()
            $reader = [System.IO.StreamReader]::new($stream)
            $body = $reader.ReadToEnd()
            $reader.Close()
            Write-Host "[FAIL] $Name - HTTP $status" -ForegroundColor Red
            Write-Host "       Error: $body" -ForegroundColor Yellow
            return @{success=$false; status=$status; error=$body}
        }
        Write-Host "[FAIL] $Name - $_" -ForegroundColor Red
        return @{success=$false; error=$_.ToString()}
    }
}

# 1. Login
Write-Host "`n=== 1. 登录认证 ===" -ForegroundColor Cyan
$r = Test-API -Name "POST /api/v1/auth/login" -Method POST -Endpoint "/api/v1/auth/login" -Body '{"username":"admin","password":"admin123"}' -Auth $false
if ($r.success) {
    $global:token = $r.data.token
    Write-Host "       Token: $($global:token.Substring(0, [Math]::Min(30, $global:token.Length)))..."
}

# 2. 部门管理 API
Write-Host "`n=== 2. 部门管理 API ===" -ForegroundColor Cyan

# 2.1 GET /api/v1/departments
$r = Test-API -Name "GET /api/v1/departments" -Method GET -Endpoint "/api/v1/departments"

# 2.2 POST /api/v1/departments
$r = Test-API -Name "POST /api/v1/departments" -Method POST -Endpoint "/api/v1/departments" -Body '{"name":"测试部门","code":"TEST001"}'
$createdId = $null
if ($r.success -and $r.data.id) {
    $createdId = $r.data.id
    Write-Host "       Created ID: $createdId"
}

# 2.3 PUT /api/v1/departments/:id
if ($createdId) {
    $r = Test-API -Name "PUT /api/v1/departments/$createdId" -Method PUT -Endpoint "/api/v1/departments/$createdId" -Body '{"name":"测试部门-已修改","code":"TEST001"}'
}

# 2.4 DELETE /api/v1/departments/:id
if ($createdId) {
    $r = Test-API -Name "DELETE /api/v1/departments/$createdId" -Method DELETE -Endpoint "/api/v1/departments/$createdId"
}

# 3. 回归测试
Write-Host "`n=== 3. 回归测试 ===" -ForegroundColor Cyan

Test-API -Name "GET /api/v1/stores" -Method GET -Endpoint "/api/v1/stores"
Test-API -Name "GET /api/v1/devices" -Method GET -Endpoint "/api/v1/devices"
Test-API -Name "GET /api/v1/dashboard/stats" -Method GET -Endpoint "/api/v1/dashboard/stats"

Write-Host "`n=== 测试完成 ===" -ForegroundColor Cyan
