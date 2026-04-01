$viewsPath = "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views"
Get-ChildItem $viewsPath -Recurse -Filter "*.vue" | ForEach-Object {
    $path = $_.FullName
    $lines = @(Get-Content $path -Encoding UTF8)
    $newLines = @()
    $inTable = $false
    $i = 0
    while ($i -lt $lines.Count) {
        $line = $lines[$i]
        if ($line -match '<a-table\s') {
            $inTable = $true
            $newLines += $line
        } elseif ($inTable -and $line -match '<a-modal\s') {
            $newLines += "      </a-table>"
            $inTable = $false
            $newLines += $line
        } elseif ($inTable -and $line -match '<template\s') {
            $newLines += $line
            $i++
            $line = $lines[$i]
            while ($i -lt $lines.Count -and $line -notmatch '</template>') {
                $newLines += $line
                $i++
                $line = $lines[$i]
            }
            if ($i -lt $lines.Count) { $newLines += $line }
            if ($line -notmatch '</a-table>') { $newLines += "      </a-table>" }
            $inTable = $false
        } elseif ($inTable -and $line -match '</a-table>') {
            $newLines += $line
            $inTable = $false
        } else {
            $newLines += $line
        }
        $i++
    }
    if (($newLines | Measure-Object).Count -ne ($lines | Measure-Object).Count) {
        Write-Host "Fixed $($_.Name) (table)"
    }
    Set-Content -Path $path -Value $newLines -Encoding UTF8
}
Write-Host "Done"
