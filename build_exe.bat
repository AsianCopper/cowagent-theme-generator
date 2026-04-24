@echo off
chcp 65001 >nul
title CowAgent 主题生成器 - 打包工具

echo 🎸 =========================================
echo    CowAgent 主题生成器 - EXE 打包工具
echo    By: 亚洲铜 x BocchiBot
echo =========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo 📝 正在安装依赖...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo.
echo 📦 正在打包 EXE 程序...
pyinstaller --onefile --windowed --name "CowAgent-ThemeGenerator" --icon=NONE ^
    --add-data "requirements.txt;." ^
    --clean ^
    theme_generator.py

if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ✅ 打包完成！
echo 📁 EXE 文件位于: dist\CowAgent-ThemeGenerator.exe
echo.
pause
