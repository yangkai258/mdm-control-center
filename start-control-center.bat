@echo off
chcp 65001 >nul
title OpenClaw 企业微信控制台
echo.
echo ========================================
echo   🦞 OpenClaw 企业微信控制台
echo ========================================
echo.

REM 检查4310端口
netstat -ano | findstr ":4310.*LISTENING" >nul
if %errorlevel%==0 (
    echo ✅ 服务已在运行
    echo.
) else (
    echo ⚙️ 端口 4310 未监听
    echo.
    echo 请确保 OpenClaw Gateway 已启动
    echo.
)

echo 📱 访问地址：
echo   http://127.0.0.1:4310/
echo.
echo ========================================
echo.

REM 显示可用端口
echo 当前 OpenClaw 监听端口：
echo.
netstat -ano | findstr "LISTENING" | findstr "4310\|3000\|8080"

echo.
pause
