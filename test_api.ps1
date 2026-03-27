param(
    [string]$Method = "GET",
    [string]$Url = "",
    [string]$Body = ""
)

$headers = @{
    "Content-Type" = "application/json"
}
if ($global:authToken) {
    $headers["Authorization"] = "Bearer $global:authToken"
}

$params = @{
    Uri = $Url
    Method = $Method
    Headers = $headers
}
if ($Body) {
    $params["Body"] = $Body
}

try {
    $response = Invoke-RestMethod @params
    $response | ConvertTo-Json -Depth 10
} catch {
    $err = $_.Exception.Response
    if ($err) {
        $reader = [System.IO.StreamReader]::new($err.GetResponseStream())
        $respBody = $reader.ReadToEnd()
        $reader.Close()
        Write-Host "ERROR: $($err.StatusCode) - $respBody"
    } else {
        Write-Host "ERROR: $_"
    }
}
