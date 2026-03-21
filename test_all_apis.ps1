$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwicm9sZV9pZCI6MSwiZXhwIjoxNzc0MTYzNDI3LCJpYXQiOjE3NzQwNzcwMjd9.echak9zvqhS36o-J5rz4b2To5YxUZRcGXNi9H_4Ycn0"
$base = "http://localhost:16666/api/v1"
$headers = @{"Authorization"="Bearer $token"}

$results = @()

function Test-API {
    param($name, $method, $path, $body=$null)
    $url = "$base$path"
    try {
        if ($method -eq "GET") {
            $r = Invoke-WebRequest -Uri $url -Headers $headers -UseBasicParsing -TimeoutSec 10
        } elseif ($method -eq "POST") {
            $r = Invoke-WebRequest -Uri $url -Method POST -Headers $headers -ContentType "application/json" -Body ($body | ConvertTo-Json) -UseBasicParsing -TimeoutSec 10
        } elseif ($method -eq "PUT") {
            $r = Invoke-WebRequest -Uri $url -Method PUT -Headers $headers -ContentType "application/json" -Body ($body | ConvertTo-Json) -UseBasicParsing -TimeoutSec 10
        } elseif ($method -eq "DELETE") {
            $r = Invoke-WebRequest -Uri $url -Method DELETE -Headers $headers -UseBasicParsing -TimeoutSec 10
        }
        $status = $r.StatusCode
        $content = $r.Content | ConvertFrom-Json
        $hasData = $null -ne $content.data
        $results += [PSCustomObject]@{ Name = $name; Method = $method; Path = $path; Status = $status; HasData = $hasData; Message = $content.message }
        Write-Host "[PASS] $method $path -> $status" -ForegroundColor Green
    } catch {
        $err = $_.Exception.Message
        if ($err -match '(\d{3})') { $status = $matches[1] } else { $status = "ERR" }
        $results += [PSCustomObject]@{ Name = $name; Method = $method; Path = $path; Status = $status; HasData = $false; Message = $err }
        Write-Host "[FAIL] $method $path -> $status : $err" -ForegroundColor Red
    }
}

# Sprint 1-4: Device Management
Test-API "设备列表" "GET" "/devices"
Test-API "设备详情" "GET" "/devices/1"
Test-API "创建设备" "POST" "/devices" @{"device_name"="test-device";"device_type"="pet_tracker";"mac_address"="AA:BB:CC:DD:EE:01"}
Test-API "更新设备" "PUT" "/devices/1" @{"device_name"="test-updated"}

# Sprint 1-4: OTA
Test-API "OTA包列表" "GET" "/ota/packages"
Test-API "OTA部署列表" "GET" "/ota/deployments"

# Sprint 1-4: Alerts
Test-API "告警列表" "GET" "/alerts"
Test-API "告警规则列表" "GET" "/alert-rules"

# Sprint 1-4: Notifications
Test-API "通知列表" "GET" "/notifications"
Test-API "公告列表" "GET" "/announcements"

# Sprint 5: Members
Test-API "会员列表" "GET" "/members"
Test-API "会员积分" "GET" "/members/points"
Test-API "优惠券列表" "GET" "/coupons"

# Sprint 7: Organization
Test-API "公司列表" "GET" "/org/companies"
Test-API "部门列表" "GET" "/org/departments"
Test-API "员工列表" "GET" "/org/employees"

# Sprint 7: Permissions
Test-API "角色列表" "GET" "/roles"
Test-API "权限列表" "GET" "/permissions"

$results | Format-Table -AutoSize
