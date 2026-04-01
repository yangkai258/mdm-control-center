Get-ChildItem "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views" -Recurse -Filter "*.vue" | ForEach-Object {
    $path = $_.FullName
    $c = Get-Content $path -Raw
    if ($c -match '<a-table\s' -and $c -notmatch '</a-table>') {
        if ($c -match '<a-modal\s') {
            $c2 = $c -replace '<a-modal\s', "</a-table>`n    <a-modal "
        } else {
            $c2 = $c -replace '</a-card>', "</a-table>`n  </a-card>"
        }
        Set-Content -Path $path -Value $c2 -Encoding UTF8
        Write-Host "Fixed $($_.Name)"
    }
}
Write-Host "Done"
