@echo off
echo ========================================
echo OpenClaw Control Center 测试启动脚本
echo ========================================
echo.

REM 检查Node.js是否安装
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 错误: Node.js 未安装或未在PATH中
    pause
    exit /b 1
)

REM 检查控制中心目录
set CONTROL_CENTER_DIR="C:\Users\YKing\Downloads\openclaw-control-center-main\openclaw-control-center-main"
if not exist %CONTROL_CENTER_DIR% (
    echo ❌ 错误: 控制中心目录不存在: %CONTROL_CENTER_DIR%
    pause
    exit /b 1
)

REM 检查package.json
if not exist %CONTROL_CENTER_DIR%\package.json (
    echo ❌ 错误: package.json 不存在
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

echo 正在启动 OpenClaw Control Center...
echo 请等待服务启动完成...
echo.

REM 切换到控制中心目录并启动
cd /d %CONTROL_CENTER_DIR%
call npm run dev

if %errorlevel% neq 0 (
    echo.
    echo ❌ 启动失败，错误代码: %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo ✅ OpenClaw Control Center 已启动
echo 访问地址: http://localhost:3000
echo.
echo 按任意键退出...
pause >nul