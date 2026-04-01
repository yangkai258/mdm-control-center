$dirs = @('store','marketing','pet-social','platform','portal','research','policies','tenants','org','health','globalization','family','offline','app','analytics')
$fixed = 0
foreach ($d in $dirs) {
    $path = "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\$d"
    if (-not (Test-Path $path)) { continue }
    Get-ChildItem $path -Filter "*.vue" -ErrorAction SilentlyContinue | ForEach-Object {
        $lines = @(Get-Content $_.FullName -Encoding UTF8)
        $newLines = @()
        $inTable = 0
        for ($i = 0; $i -lt $lines.Length; $i++) {
            $line = $lines[$i]
            if ($line -match '<a-table\s') {
                $inTable = 1
                $newLines += $line
            } elseif ($inTable -eq 1 -and $line -match '<a-modal\s') {
                $newLines += "      </a-table>"
                $inTable = 0
                $newLines += $line
            } elseif ($inTable -eq 1 -and $line -match '<template\s') {
                $newLines += $line
                $inTable = 2
            } elseif ($inTable -eq 2 -and $line -match '</template>') {
                $newLines += $line
                $inTable = 1
            } elseif ($inTable -eq 1 -and $line -match '</a-table>') {
                $newLines += $line
                $inTable = 0
            } else {
                $newLines += $line
            }
        }
        $lastIdx = $newLines.Count - 1
        if ($newLines[$lastIdx] -notmatch '</a-card>' -and $newLines[$lastIdx-1] -match '</div>') {
            $newLines[$lastIdx-1] = '  </a-card>'
            $newLines += '</a-card>'
        }
        Set-Content -Path $_.FullName -Value $newLines -Encoding UTF8
        $fixed++
    }
}
Write-Host "Done: $fixed files"
