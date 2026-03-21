# V2.2规范检查脚本
param(
    [string]$FilePath
)

$content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
if (-not $content) { return "ERROR: Cannot read file" }

$issues = @()
$checks = @()

# 1. 检查表格是否有row-selection
if ($content -match 'row-selection.*checkbox|checkbox.*row-selection') {
    $checks += "✅ 多选框"
} else {
    $issues += "❌ 缺少row-selection多选框"
}

# 2. 检查名称/id是否可点击(a-link)
if ($content -match 'a-link.*@click|<a-link.*@click') {
    $checks += "✅ 名称可点击"
} else {
    $issues += "⚠️ 可能缺少名称可点击"
}

# 3. 检查是否有a-modal详情弹窗
if ($content -match 'a-modal.*title=.*详情|openDetail|detailVisible') {
    $checks += "✅ 详情弹窗"
} else {
    $issues += "⚠️ 可能缺少详情弹窗"
}

# 4. 检查操作栏按钮布局
$hasNew = $content -match '新建|新建'
$hasEdit = $content -match '编辑'
$hasDelete = $content -match '删除'

if ($hasNew -and $hasEdit -and $hasDelete) {
    $checks += "✅ 主操作按钮完整"
} elseif ($hasNew) {
    $issues += "⚠️ 缺少部分主操作按钮"
}

# 5. 检查是否有批量操作
if ($content -match '批量导入|批量删除|handleBatch') {
    $checks += "✅ 批量操作"
}

# 6. 检查是否有分页
if ($content -match 'pagination|@page-change') {
    $checks += "✅ 分页"
}

$result = @{
    File = Split-Path $FilePath -Leaf
    Checks = $checks
    Issues = $issues
}
return $result
