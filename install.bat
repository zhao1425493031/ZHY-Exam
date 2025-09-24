@echo off
chcp 65001 >nul
echo 🚀 开始安装在线考试系统...

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查pip是否安装
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip未安装，请先安装pip
    pause
    exit /b 1
)

:: 创建虚拟环境
echo 📦 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo ❌ 创建虚拟环境失败
    pause
    exit /b 1
)

:: 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

:: 升级pip
echo 📈 升级pip...
python -m pip install --upgrade pip

:: 安装依赖
echo 📚 安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 安装依赖失败
    pause
    exit /b 1
)

:: 创建必要目录
echo 📁 创建必要目录...
if not exist uploads mkdir uploads
if not exist logs mkdir logs

:: 复制环境变量文件
if not exist .env (
    echo 📝 创建环境变量文件...
    copy env.example .env
    echo ⚠️  请编辑 .env 文件，配置数据库和邮箱信息
    echo    特别是以下配置项：
    echo    - SECRET_KEY: 应用密钥
    echo    - DATABASE_URL: 数据库连接
    echo    - MAIL_USERNAME: 邮箱用户名
    echo    - MAIL_PASSWORD: 邮箱授权码
    echo.
    pause
)

:: 初始化数据库
echo 🗄️  初始化数据库...
python init_database.py

echo ✅ 安装完成！
echo.
echo 🌐 启动服务: run.bat
echo 👤 管理员账号: admin@example.com
echo 🔑 管理员密码: admin123
echo.
pause
