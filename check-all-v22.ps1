$base = "C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views"
$pages = @(
    'alerts\AlertList.vue',
    'alerts\AlertRules.vue',
    'alerts\AlertSettings.vue',
    'apps\AppList.vue',
    'apps\AppDistributions.vue',
    'apps\AppVersions.vue',
    'knowledge\KnowledgeList.vue',
    'members\MemberPoints.vue',
    'members\MemberCoupons.vue',
    'members\MemberPromotions.vue',
    'miniclaw\FirmwareList.vue',
    'notifications\NotificationList.vue',
    'notifications\Announcements.vue',
    'notifications\NotificationTemplates.vue',
    'org\Companies.vue',
    'org\Departments.vue',
    'org\Posts.vue',
    'org\StandardPositions.vue',
    'org\Employees.vue',
    'permissions\Roles.vue',
    'permissions\Menus.vue',
    'permissions\ApiPermissions.vue',
    'permissions\DataPermissionConfig.vue',
    'permissions\PermissionGroups.vue',
    'pet\PetConsole.vue',
    'pet\PetConversations.vue',
    'policies\PolicyList.vue',
    'policies\PolicyConfigs.vue',
    'policies\ComplianceRules.vue',
    'system\Monitor.vue',
    'tenants\TenantApproval.vue',
    'tenants\TenantManagement.vue',
    'tenants\TenantSettings.vue',
    'tenants\PublicArchives.vue',
    'tenants\SystemInfo.vue',
    'ota\OtaPackages.vue',
    'ota\OtaDeployments.vue',
    'Dashboard.vue',
    'Alert.vue',
    'Member.vue',
    'OtaFirmware.vue',
    'PetConfig.vue',
    'DeviceDashboard.vue',
    'DeviceList.vue',
    'DeviceDetail.vue',
    'DeviceStatus.vue'
)

$pass = 0
$fail = 0
$skip = 0

foreach ($p in $pages) {
    $f = Join-Path $base $p
    if (-not (Test-Path $f)) {
        Write-Host "[跳过] $p - 文件不存在"
        $skip++
        continue
    }
    
    $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    if (-not $content) {
        Write-Host "[错误] $p - 无法读取"
        $fail++
        continue
    }
    
    $checks = @()
    $issues = @()
    
    # 1. row-selection
    if ($content -match 'row-selection') {
        $checks += "☑"
    } else {
        $issues += "□"
    }
    
    # 2. a-link点击
    if ($content -match '<a-link.*@click|@click.*openDetail|@click=.*open') {
        $checks += "☑"
    } else {
        $issues += "□"
    }
    
    # 3. 详情弹窗
    if ($content -match 'detail.*visible|openDetail|a-modal.*title' -and $content -match 'a-modal') {
        $checks += "☑"
    } else {
        $issues += "□"
    }
    
    # 4. 主操作按钮
    $hasNew = $content -match '新建|openCreate'
    $hasEdit = $content -match '编辑|openEdit'
    $hasDel = $content -match '删除|handleDelete'
    if ($hasNew -and $hasEdit -and $hasDel) {
        $checks += "☑"
    } elseif ($hasNew -or $hasEdit -or $hasDel) {
        $checks += "◑"
    } else {
        $issues += "□"
    }
    
    # 5. 批量操作
    if ($content -match 'batch.*delete|batchDelete|批量') {
        $checks += "☑"
    } else {
        $checks += "○"
    }
    
    # 6. API连接
    if ($content -match 'from.*@/api|import.*api/') {
        $checks += "☑"
    } else {
        $issues += "□"
    }
    
    $status = if ($issues.Count -eq 0) { "✅" } else { "⚠️" }
    $checkStr = ($checks -join " ")
    $issueStr = if ($issues.Count -gt 0) { " | $status $issueStr" } else { "" }
    
    Write-Host "$status $($checks -join ' ')`t$p"
    if ($issues.Count -gt 0) {
        Write-Host "       问题: $($issues -join ', ')"
    }
    
    if ($issues.Count -eq 0) { $pass++ } else { $fail++ }
}

Write-Host ""
Write-Host "============================================"
Write-Host "检查完成: ✅$pass  ⚠️$fail  跳过$skip"
Write-Host "============================================"
