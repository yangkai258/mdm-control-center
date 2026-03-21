$html = (Invoke-WebRequest -Uri 'https://blog.csdn.net/m0_57344393/article/details/144404709' -UseBasicParsing).Content
if ($html -match 'img[^>]+src="([^"]+)"') {
    $matches = [regex]::Matches($html, 'img[^>]+src="([^"]+)"')
    foreach ($m in $matches) {
        Write-Host $m.Groups[1].Value
    }
}
