$ErrorActionPreference = "Continue"
$baseUrl = "http://localhost:8080"
$global:token = ""

function Get-ResponseBody {
    param($response)
    try {
        $stream = $response.GetResponseStream()
        $reader = [System.IO.StreamReader]::new($stream)
        $body = $reader.ReadToEnd()
        $reader.Close()
        return $body
    } catch { return "N/A" }
}

function Test-API {
    param([string]$Name, [string]$Method, [string]$Endpoint, [string]$Body = "", [bool]$NeedAuth = $true)
    $url = "$baseUrl$Endpoint"
    $results = @{}
    
    try {
        $wr = [System.Net.WebRequest]::CreateHttp($url)
        $wr.Method = $Method
        $wr.ContentType = "application/json"
        if ($NeedAuth -and $global:token) {
            $wr.Headers["Authorization"] = "Bearer $global:token"
        }
        
        if ($Body) {
            $bytes = [System.Text.Encoding]::UTF8.GetBytes($Body)
            $wr.ContentLength = $bytes.Length
            $reqStream = $wr.GetRequestStream()
            $reqStream.Write($bytes, 0, $bytes.Length)
            $reqStream.Close()
        }
        
        $resp = $wr.GetResponse()
        $respStream = $resp.GetResponseStream()
        $reader = [System.IO.StreamReader]::new($respStream)
        $content = $reader.ReadToEnd()
        $reader.Close()
        $resp.Close()
        
        $status = [int]$resp.StatusCode
        $json = $null
        try { $json = $content | ConvertFrom-Json } catch {}
        
        if ($status -ge 200 -and $status -lt 300) {
            Write-Host "[PASS] $Name | HTTP $status" -ForegroundColor Green
            $results.success = $true
            $results.status = $status
            $results.data = $json
        } else {
            Write-Host "[FAIL] $Name | HTTP $status" -ForegroundColor Red
            Write-Host "       Body: $($content.Substring(0, [Math]::Min(300, $content.Length)))" -ForegroundColor Yellow
            $results.success = $false
            $results.status = $status
            $results.error = $content
        }
    } catch {
        $ex = $_.Exception
        $status = 0
        $errBody = ""
        if ($ex.Response) {
            $status = [int]$ex.Response.StatusCode
            $errBody = Get-ResponseBody($ex.Response)
        }
        Write-Host "[FAIL] $Name | HTTP $status | $($ex.Message)" -ForegroundColor Red
        if ($errBody) {
            Write-Host "       Body: $($errBody.Substring(0, [Math]::Min(200, $errBody.Length)))" -ForegroundColor Yellow
        }
        $results.success = $false
        $results.status = $status
        $results.error = $errBody
    }
    return $results
}

# ========== 1. 登录认证 ==========
Write-Host "`n========== 1. 登录认证 ==========" -ForegroundColor Cyan
$body = '{"username":"admin","password":"admin123"}'
try {
    $wr = [System.Net.WebRequest]::CreateHttp("$baseUrl/api/v1/auth/login")
    $wr.Method = "POST"
    $wr.ContentType = "application/json"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    $wr.ContentLength = $bytes.Length
    $reqStream = $wr.GetRequestStream()
    $reqStream.Write($bytes, 0, $bytes.Length)
    $reqStream.Close()
    $resp = $wr.GetResponse()
    $reader = [System.IO.StreamReader]::new($resp.GetResponseStream())
    $content = $reader.ReadToEnd()
    $reader.Close(); $resp.Close()
    $json = $content | ConvertFrom-Json
    $global:token = $json.data.token
    Write-Host "[PASS] POST /api/v1/auth/login | HTTP 200" -ForegroundColor Green
    Write-Host "       User: $($json.data.username) | Token: $($global:token.Substring(0,30))..." -ForegroundColor Gray
} catch {
    Write-Host "[FAIL] POST /api/v1/auth/login | Login failed: $_" -ForegroundColor Red
    Write-Host "       === 测试中止 ===" -ForegroundColor Red
    exit 1
}

# ========== 2. 部门管理 API ==========
Write-Host "`n========== 2. 部门管理 API ==========" -ForegroundColor Cyan
$pass = 0; $fail = 0

# 2.1 GET departments
$r = Test-API -Name "GET /api/v1/departments" -Method GET -Endpoint "/api/v1/departments"
if ($r.success) { $pass++ } else { $fail++ }
$deptList = $r.data

# 2.2 POST department
$body = '{"name":"测试部门","code":"TEST001"}'
$r = Test-API -Name "POST /api/v1/departments" -Method POST -Endpoint "/api/v1/departments" -Body $body
if ($r.success) { $pass++ } else { $fail++ }
$newId = $null
if ($r.success -and $r.data.data.id) { $newId = $r.data.data.id }

# 2.3 PUT department
if ($newId) {
    $body = '{"name":"测试部门-已修改","code":"TEST001-MODIFIED"}'
    $r = Test-API -Name "PUT /api/v1/departments/$newId" -Method PUT -Endpoint "/api/v1/departments/$newId" -Body $body
    if ($r.success) { $pass++ } else { $fail++ }
} else {
    Write-Host "[SKIP] PUT /api/v1/departments/:id (no ID from create)" -ForegroundColor Gray
    $fail++
}

# 2.4 DELETE department
if ($newId) {
    $r = Test-API -Name "DELETE /api/v1/departments/$newId" -Method DELETE -Endpoint "/api/v1/departments/$newId"
    if ($r.success) { $pass++ } else { $fail++ }
} else {
    Write-Host "[SKIP] DELETE /api/v1/departments/:id (no ID from create)" -ForegroundColor Gray
    $fail++
}

# ========== 3. 回归测试 ==========
Write-Host "`n========== 3. 回归测试 ==========" -ForegroundColor Cyan

$r = Test-API -Name "GET /api/v1/stores" -Method GET -Endpoint "/api/v1/stores"
if ($r.success) { $pass++ } else { $fail++ }

$r = Test-API -Name "GET /api/v1/devices" -Method GET -Endpoint "/api/v1/devices"
if ($r.success) { $pass++ } else { $fail++ }

$r = Test-API -Name "GET /api/v1/dashboard/stats" -Method GET -Endpoint "/api/v1/dashboard/stats"
if ($r.success) { $pass++ } else { $fail++ }

# ========== 结果汇总 ==========
Write-Host "`n========== 测试结果汇总 ==========" -ForegroundColor Cyan
Write-Host "通过: $pass / $($pass+$fail)" -ForegroundColor Green
Write-Host "失败: $fail / $($pass+$fail)" -ForegroundColor $(if($fail -gt 0){"Red"}else{"Green"})
if ($fail -eq 0) {
    Write-Host "结论: ALL PASS ✓" -ForegroundColor Green
} else {
    Write-Host "结论: 有失败项，需要检查" -ForegroundColor Red
}
