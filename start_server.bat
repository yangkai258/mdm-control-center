@echo off
echo ========================================
echo MBTI测试服务器启动脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.x
    pause
    exit /b 1
)

echo ✅ Python已安装
echo.

REM 检查必要模块
echo 检查必要模块...
python -c "import sqlite3, hashlib, json, time, jwt, secrets, datetime, http.server, urllib.parse, os" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少必要模块，正在安装...
    pip install pyjwt
    if errorlevel 1 (
        echo ❌ 安装模块失败
        pause
        exit /b 1
    )
    echo ✅ 模块安装完成
) else (
    echo ✅ 所有必要模块已安装
)

echo.

REM 启动服务器
echo 🚀 正在启动MBTI测试服务器...
echo 📍 端口: 8004
echo 🌐 访问地址: http://localhost:8004
echo 📁 数据库: mbti_test.db
echo.

echo 按 Ctrl+C 停止服务器
echo.

python complete_server.py

if errorlevel 1 (
    echo.
    echo ❌ 服务器启动失败
    echo 💡 可能的原因:
    echo   1. 端口8004已被占用
    echo   2. 缺少必要权限
    echo   3. 代码有语法错误
    echo.
    pause
)