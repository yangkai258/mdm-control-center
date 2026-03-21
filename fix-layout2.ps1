# Fix Vue files with a-layout-content issues
$files = Get-ChildItem -Path "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views" -Recurse -Include "*.vue"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    
    # Skip if no a-layout-content found
    if ($content -notmatch 'a-layout-content') {
        continue
    }
    
    Write-Host "Fixing: $($file.Name)"
    
    # Remove a-layout-content opening tag (keep content)
    $content = $content -replace '<a-layout-content\s+class="content">\s*', '<div class="page-content">'
    $content = $content -replace '<a-layout-content\s*>', '<div class="page-content">'
    
    # Remove a-layout-content closing tag
    $content = $content -replace '\s*</a-layout-content>', '</div>'
    
    # Remove any remaining a-layout tags (empty ones or wrappers)
    $content = $content -replace '<a-layout\s+class="[^"]*">\s*</a-layout>', ''
    $content = $content -replace '<a-layout>\s*</a-layout>', ''
    $content = $content -replace '</a-layout>', ''
    
    # Remove empty lines that might be left over
    $content = $content -replace '\n\s*\n\s*\n', "`n`n"
    
    Set-Content -Path $file.FullName -Value $content -NoNewline -Encoding UTF8
    Write-Host "  Done"
}

Write-Host "All files fixed"
