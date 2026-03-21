# PowerShell script to remove a-layout from Vue files
$files = @(
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertList.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertRules.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\alerts\AlertSettings.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppDistributions.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppList.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\apps\AppVersions.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\members\MemberCoupons.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\members\MemberPromotions.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\policies\ComplianceRules.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\policies\PolicyConfigs.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\policies\PolicyList.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\DeviceDashboard.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\DeviceDetail.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\DeviceStatus.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\OtaFirmware.vue",
    "C:\Users\YKing\.openclaw\workspace\mdm-project\frontend\src\views\PetConfig.vue"
)

foreach ($file in $files) {
    Write-Host "Processing: $file"
    $content = Get-Content $file -Raw
    
    # Skip if already processed (no a-layout-sider)
    if ($content -notmatch 'a-layout-sider') {
        Write-Host "  Already processed or no a-layout-sider found"
        continue
    }
    
    # Remove a-layout-sider block
    $content = $content -replace '<a-layout-sider[^>]*>[\s\S]*?</a-layout-sider>', ''
    
    # Remove outer a-layout and keep only content
    # Pattern: <a-layout class="xxx"> ... </a-layout>
    $content = $content -replace '<a-layout\s+class="[^"]*">\s*<a-layout-content\s+class="content">', '<div class="page-container">'
    $content = $content -replace '</a-layout-content>\s*</a-layout>', '</div>'
    
    # Also handle a-layout without class
    $content = $content -replace '<a-layout>\s*<a-layout-content\s+class="content">', '<div class="page-container">'
    $content = $content -replace '</a-layout-content>\s*</a-layout>', '</div>'
    
    # Remove a-layout-header if exists (between sider and content)
    $content = $content -replace '<a-layout-header[^>]*>[\s\S]*?</a-layout-header>', ''
    
    # Remove remaining a-layout tags
    $content = $content -replace '</a-layout>', ''
    
    # Remove router import if not needed
    $content = $content -replace "import\s+\{[^}]*\}\s+from\s+'vue-router'\s*", ''
    
    # Remove useRouter if not used
    $content = $content -replace "const\s+router\s*=\s*useRouter\(\)\s*", ''
    
    # Remove handleMenuClick if exists
    $content = $content -replace 'const\s+handleMenuClick\s*=\s*\([^)]*\)\s*=>\s*\{[\s\S]*?\}\s*', ''
    
    # Remove selectedKeys and collapsed refs if only used by removed menu
    $content = $content -replace "const\s+selectedKeys\s*=\s*ref\([^)]*\)\s*", ''
    $content = $content -replace "const\s+collapsed\s*=\s*ref\([^)]*\)\s*", ''
    
    # Update style: remove min-height: 100vh from page-container
    $content = $content -replace '\.page-container\s*\{', '.page-container {'
    
    Set-Content -Path $file -Value $content -NoNewline
    Write-Host "  Done"
}

Write-Host "All files processed"
