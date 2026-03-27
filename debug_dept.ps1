$ErrorActionPreference = "Continue"
$baseUrl = "http://localhost:8080"

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

# Login first
$body = '{"username":"admin","password":"admin123"}'
$wr = [System.Net.WebRequest]::CreateHttp("$baseUrl/api/v1/auth/login")
$wr.Method = "POST"; $wr.ContentType = "application/json"
$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
$wr.ContentLength = $bytes.Length
$reqStream = $wr.GetRequestStream(); $reqStream.Write($bytes,0,$bytes.Length); $reqStream.Close()
$resp = $wr.GetResponse()
$reader = [System.IO.StreamReader]::new($resp.GetResponseStream()); $content = $reader.ReadToEnd(); $reader.Close(); $resp.Close()
$token = ($content | ConvertFrom-Json).data.token

# Debug GET /api/v1/departments
Write-Host "=== GET /api/v1/departments ==="
try {
    $wr2 = [System.Net.WebRequest]::CreateHttp("$baseUrl/api/v1/departments")
    $wr2.Method = "GET"
    $wr2.Headers["Authorization"] = "Bearer $token"
    $resp2 = $wr2.GetResponse()
    $reader2 = [System.IO.StreamReader]::new($resp2.GetResponseStream())
    $content2 = $reader2.ReadToEnd()
    $reader2.Close(); $resp2.Close()
    Write-Host "Status: $([int]$resp2.StatusCode)"
    Write-Host "Body: $content2"
} catch {
    $ex = $_.Exception
    Write-Host "Exception: $($ex.Message)"
    if ($ex.Response) {
        Write-Host "Status: $([int]$ex.Response.StatusCode)"
        Write-Host "Body: $(Get-ResponseBody($ex.Response))"
    }
}

# Debug POST /api/v1/departments
Write-Host "`n=== POST /api/v1/departments ==="
try {
    $wr3 = [System.Net.WebRequest]::CreateHttp("$baseUrl/api/v1/departments")
    $wr3.Method = "POST"
    $wr3.ContentType = "application/json"
    $wr3.Headers["Authorization"] = "Bearer $token"
    $body3 = '{"name":"测试部门","code":"TEST001"}'
    $bytes3 = [System.Text.Encoding]::UTF8.GetBytes($body3)
    $wr3.ContentLength = $bytes3.Length
    $reqStream3 = $wr3.GetRequestStream(); $reqStream3.Write($bytes3,0,$bytes3.Length); $reqStream3.Close()
    $resp3 = $wr3.GetResponse()
    $reader3 = [System.IO.StreamReader]::new($resp3.GetResponseStream())
    $content3 = $reader3.ReadToEnd()
    $reader3.Close(); $resp3.Close()
    Write-Host "Status: $([int]$resp3.StatusCode)"
    Write-Host "Body: $content3"
} catch {
    $ex = $_.Exception
    Write-Host "Exception: $($ex.Message)"
    if ($ex.Response) {
        Write-Host "Status: $([int]$ex.Response.StatusCode)"
        Write-Host "Body: $(Get-ResponseBody($ex.Response))"
    }
}
