$base = "C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views"
$pages = @(
    "alerts\AlertList.vue",
    "alerts\AlertRules.vue",
    "alerts\AlertSettings.vue",
    "apps\AppList.vue",
    "apps\AppDistributions.vue",
    "apps\AppVersions.vue",
    "knowledge\KnowledgeList.vue",
    "members\MemberPoints.vue",
    "members\MemberCoupons.vue",
    "members\MemberPromotions.vue",
    "miniclaw\FirmwareList.vue",
    "notifications\NotificationList.vue",
    "notifications\Announcements.vue",
    "notifications\NotificationTemplates.vue",
    "org\Companies.vue",
    "org\Departments.vue",
    "org\Posts.vue",
    "org\StandardPositions.vue",
    "org\Employees.vue",
    "permissions\Roles.vue",
    "permissions\Menus.vue",
    "permissions\ApiPermissions.vue",
    "permissions\DataPermissionConfig.vue",
    "permissions\PermissionGroups.vue",
    "pet\PetConsole.vue",
    "pet\PetConversations.vue",
    "policies\PolicyList.vue",
    "policies\PolicyConfigs.vue",
    "policies\ComplianceRules.vue",
    "system\Monitor.vue",
    "tenants\TenantApproval.vue",
    "tenants\TenantManagement.vue",
    "tenants\TenantSettings.vue",
    "tenants\PublicArchives.vue",
    "tenants\SystemInfo.vue",
    "ota\OtaPackages.vue",
    "ota\OtaDeployments.vue",
    "Dashboard.vue",
    "Alert.vue",
    "Member.vue",
    "OtaFirmware.vue",
    "PetConfig.vue",
    "DeviceDashboard.vue",
    "DeviceList.vue",
    "DeviceDetail.vue",
    "DeviceStatus.vue"
)

$pass = 0
$fail = 0
$skip = 0

Write-Host "============================================"
Write-Host "V2.2 Compliance Check - All Pages"
Write-Host "============================================"
Write-Host ""

foreach ($p in $pages) {
    $f = Join-Path $base $p
    if (-not (Test-Path $f)) {
        Write-Host "[SKIP] $p - File not found"
        $skip++
        continue
    }

    $content = Get-Content $f -Raw -ErrorAction SilentlyContinue
    if (-not $content) {
        Write-Host "[ERROR] $p - Cannot read file"
        $fail++
        continue
    }

    $checks = @()
    $issues = @()

    # 1. row-selection checkbox
    if ($content -match 'row-selection') {
        $checks += "[OK]"
    } else {
        $issues += "[MISSING row-selection]"
    }

    # 2. a-link click for detail
    if ($content -match '<a-link' -and $content -match '@click') {
        $checks += "[OK]"
    } elseif ($content -match 'openDetail') {
        $checks += "[OK]"
    } else {
        $issues += "[MISSING a-link click]"
    }

    # 3. Detail modal
    if ($content -match 'detail.*visible' -or ($content -match 'a-modal' -and $content -match 'title')) {
        $checks += "[OK]"
    } else {
        $issues += "[MISSING detail modal]"
    }

    # 4. Main action buttons (new/edit/delete)
    $hasNew = $content -match '新建|openCreate|showCreate'
    $hasEdit = $content -match '编辑|openEdit|showEdit'
    $hasDel = $content -match '删除|handleDelete|batchDelete'
    if ($hasNew -and $hasEdit -and $hasDel) {
        $checks += "[OK]"
    } elseif ($hasNew -or $hasEdit -or $hasDel) {
        $checks += "[PARTIAL]"
    } else {
        $issues += "[MISSING action buttons]"
    }

    # 5. API connection
    if ($content -match 'from.*@/api|import.*api/' -or $content -match 'axios') {
        $checks += "[API]"
    } else {
        $issues += "[NO API]"
    }

    $checkStr = ($checks -join " ")
    $issueStr = ($issues -join " ")

    if ($issues.Count -eq 0) {
        Write-Host "[PASS] $checkStr  $p"
        $pass++
    } else {
        Write-Host "[FAIL] $checkStr  $p"
        Write-Host "        ISSUES: $issueStr"
        $fail++
    }
}

Write-Host ""
Write-Host "============================================"
Write-Host "Results: PASS=$pass  FAIL=$fail  SKIP=$skip"
Write-Host "============================================"
