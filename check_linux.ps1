$bytes = [System.IO.File]::ReadAllBytes('C:\Users\YKing\.openclaw\workspace\mdm-project\backend\mdm-server-linux.exe')[0..4]
foreach ($b in $bytes) {
    Write-Host ("{0:X2}" -f $b)
}
