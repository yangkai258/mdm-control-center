$files = @(
    'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDashboard.vue',
    'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceStatus.vue',
    'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\PetConfig.vue',
    'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\OtaFirmware.vue',
    'C:\Users\YKing\.openclaw\workspace\mdm-project\mdm-frontend-new\arco-design-pro-vite\src\views\DeviceDetail.vue'
)

foreach ($f in $files) {
    if (Test-Path $f) {
        $content = Get-Content $f -Raw -Encoding UTF8
        $orig = $content
        
        $content = $content -replace '>新建</a-button>', '>「新建」</a-button>'
        $content = $content -replace '>编辑</a-button>', '>「编辑」</a-button>'
        $content = $content -replace '>删除</a-button>', '>「删除」</a-button>'
        $content = $content -replace '>批量导入</a-button>', '>「批量导入」</a-button>'
        $content = $content -replace '>导出</a-button>', '>「导出」</a-button>'
        $content = $content -replace '>刷新</a-button>', '>「刷新」</a-button>'
        $content = $content -replace '>保存</a-button>', '>「保存」</a-button>'
        $content = $content -replace '>取消</a-button>', '>「取消」</a-button>'
        $content = $content -replace '>创建</a-button>', '>「创建」</a-button>'
        $content = $content -replace '>查询</a-button>', '>「查询」</a-button>'
        $content = $content -replace '>重置</a-button>', '>「重置」</a-button>'
        $content = $content -replace '>确认</a-button>', '>「确认」</a-button>'
        $content = $content -replace '>详情</a-button>', '>「详情」</a-button>'
        $content = $content -replace '>分配权限</a-button>', '>「分配权限」</a-button>'
        $content = $content -replace '>新增下级</a-button>', '>「新增下级」</a-button>'
        
        if ($content -ne $orig) {
            $content | Set-Content $f -Encoding UTF8
            $name = Split-Path $f -Leaf
            Write-Host "Fixed: $name"
        } else {
            $name = Split-Path $f -Leaf
            Write-Host "No change: $name"
        }
    }
}
Write-Host "Done"
