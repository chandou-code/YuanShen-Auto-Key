@echo off
chcp 65001 > nul
set "PYTHON_PROJECT=C:\Users\10717\PycharmProjects\空格F"

REM 检查虚拟环境
if not exist "%PYTHON_PROJECT%\.venv\Scripts\activate.bat" (
    echo 错误：虚拟环境不存在于以下路径：
    echo %PYTHON_PROJECT%\.venv
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 正在激活虚拟环境...
if exist "%PYTHON_PROJECT%\.venv\Scripts\activate.bat" (
    call "%PYTHON_PROJECT%\.venv\Scripts\activate.bat"
    if errorlevel 1 (
        echo 激活虚拟环境失败！
        pause
        exit /b 1
    )
) else (
    echo 未找到虚拟环境，使用全局Python环境...
)

REM 确保依赖已安装
echo 正在检查并安装依赖...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo 依赖安装失败！
    pause
    exit /b 1
)

REM 运行脚本
echo 正在运行脚本...
cd /d "%PYTHON_PROJECT%"
python 空格F启动.py

REM 保持窗口
echo 执行完成
