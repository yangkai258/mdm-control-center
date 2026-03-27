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
    } catch {
        return "N/A"
    }
}

# Login
Write-Host "=== Login ==="
$body = '{"username":"admin","password":"admin123"}'
try {
    $wr = [System.Net.WebRequest]::CreateHttp("http://localhost:8080/api/v1/auth/login")
    $wr.Method = "POST"
    $wr.ContentType = "application/json"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    $wr.ContentLength = $bytes.Length
    $reqStream = $wr.GetRequestStream()
    $reqStream.Write($bytes, 0, $bytes.Length)
    $reqStream.Close()
    
    $resp = $wr.GetResponse()
    $respStream = $resp.GetResponseStream()
    $reader = [System.IO.StreamReader]::new($respStream)
    $content = $reader.ReadToEnd()
    $reader.Close()
    $resp.Close()
    
    Write-Host "Status: $($resp.StatusCode)"
    Write-Host "Content: $content"
    
    $json = $content | ConvertFrom-Json
    $global:token = $json.token
    Write-Host "Token: $global:token"
} catch {
    $ex = $_.Exception
    Write-Host "Exception: $($ex.Message)"
    if ($ex.InnerException) {
        Write-Host "Inner: $($ex.InnerException.Message)"
    }
    if ($ex.Response) {
        Write-Host "Response Status: $([int]$ex.Response.StatusCode)"
        $body2 = Get-ResponseBody($ex.Response)
        Write-Host "Response Body: $body2"
    }
}

# Now test with token
if ($global:token) {
    Write-Host "`n=== GET /api/v1/departments ==="
    try {
        $wr2 = [System.Net.WebRequest]::CreateHttp("http://localhost:8080/api/v1/departments")
        $wr2.Method = "GET"
        $wr2.Headers["Authorization"] = "Bearer $global:token"
        
        $resp2 = $wr2.GetResponse()
        $reader2 = [System.IO.StreamReader]::new($resp2.GetResponseStream())
        $content2 = $reader2.ReadToEnd()
        $reader2.Close()
        $resp2.Close()
        
        Write-Host "Status: $($resp2.StatusCode)"
        Write-Host "Content: $content2"
    } catch {
        $ex2 = $_.Exception
        Write-Host "Exception: $($ex2.Message)"
        if ($ex2.Response) {
            Write-Host "Response Status: $([int]$ex2.Response.StatusCode)"
            $body2 = Get-ResponseBody($ex2.Response)
            Write-Host "Response Body: $body2"
        }
    }
}
