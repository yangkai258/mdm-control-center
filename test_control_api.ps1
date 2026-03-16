# 测试OpenClaw Control Center控制API
Write-Host "测试OpenClaw Control Center控制API" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# 测试URL
$url = "http://127.0.0.1:4310/api/control"

# 测试数据
$testActions = @(
    @{action = "stop-control-center"},
    @{action = "restart-control-center"},
    @{action = "stop-openclaw"},
    @{action = "restart-openclaw"}
)

foreach ($testData in $testActions) {
    $action = $testData.action
    Write-Host "`n测试动作: $action" -ForegroundColor Yellow
    
    try {
        # 发送POST请求
        $response = Invoke-RestMethod -Uri $url -Method Post -Headers @{
            "Content-Type" = "application/json"
        } -Body ($testData | ConvertTo-Json) -ErrorAction Stop
        
        Write-Host "✅ 成功! 响应: $($response.message)" -ForegroundColor Green
        Write-Host "   状态: $($response.ok)" -ForegroundColor Green
        Write-Host "   动作: $($response.action)" -ForegroundColor Green
        
    } catch {
        Write-Host "❌ 错误! 状态码: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "   错误信息: $($_.Exception.Message)" -ForegroundColor Red
        
        # 尝试获取错误详情
        try {
            $errorStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($errorStream)
            $errorBody = $reader.ReadToEnd()
            Write-Host "   错误详情: $errorBody" -ForegroundColor Red
        } catch {
            Write-Host "   无法获取错误详情" -ForegroundColor Red
        }
    }
    
    Start-Sleep -Seconds 1
}

Write-Host "`n测试完成!" -ForegroundColor Cyan
Write-Host "现在可以在浏览器中测试控制按钮了:" -ForegroundColor Cyan
Write-Host "访问: http://127.0.0.1:4310" -ForegroundColor Cyan
Write-Host "点击四个控制按钮进行测试" -ForegroundColor Cyan