@echo off
echo ========================================
echo 🏢 智能体协作项目管理平台
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
python -c "import sqlite3, json, datetime, http.server, urllib.parse, secrets" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少基础模块
    pause
    exit /b 1
) else (
    echo ✅ 基础模块已安装
)

echo.

REM 启动服务器
echo 🚀 正在启动智能体协作项目管理平台...
echo 📍 端口: 8005
echo 🌐 访问地址: http://localhost:8005
echo 📁 数据库: agent_management.db
echo 👥 智能体: 6个 (主管、后端、前端、测试、产品、运维)
echo ⏰ 更新周期: 每30分钟
echo 🧠 记忆整理: 每4小时
echo.

echo 📊 功能说明:
echo   1. 实时查看6个智能体的工作进展
echo   2. 每30分钟自动/手动更新工作记录
echo   3. 可视化展示各模块工作内容
echo   4. 支持工作记录导出和模拟
echo.

echo 🔄 操作指南:
echo   1. 打开浏览器访问 http://localhost:8005
echo   2. 点击"模拟智能体工作"生成初始数据
echo   3. 每30分钟查看智能体工作更新
echo   4. 使用"导出工作报告"保存进度
echo.

echo 按 Ctrl+C 停止服务器
echo.

python agent_management_system.py

if errorlevel 1 (
    echo.
    echo ❌ 服务器启动失败
    echo 💡 可能的原因:
    echo   1. 端口8005已被占用
    echo   2. 缺少必要权限
    echo   3. 代码有语法错误
    echo.
    pause
)