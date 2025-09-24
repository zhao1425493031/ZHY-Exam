@echo off
chcp 65001 >nul
echo 🚀 启动在线考试系统...

:: 检查虚拟环境是否存在
if not exist venv (
    echo ❌ 虚拟环境不存在，请先运行 install.bat
    pause
    exit /b 1
)

:: 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

:: 检查环境变量文件
if not exist .env (
    echo ❌ 环境变量文件不存在，请先运行 install.bat
    pause
    exit /b 1
)

:: 启动应用
echo 🌐 启动Web服务...
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务
echo.
python app.py
