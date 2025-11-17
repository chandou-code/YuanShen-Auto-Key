@echo off
chcp 65001 > nul
echo === YuanShen 自动按键工具 - 便携环境创建器 ===
echo.

set "PROJECT_DIR=%~dp0"
set "PORTABLE_DIR=%PROJECT_DIR%便携版"
set "PYTHON_DIR=%PORTABLE_DIR%python"
set "PACKAGES_DIR=%PROJECT_DIR%packages"

echo 正在创建便携环境...

REM 创建目录
if not exist "%PORTABLE_DIR%" mkdir "%PORTABLE_DIR%"
if not exist "%PYTHON_DIR%" mkdir "%PYTHON_DIR%"
if not exist "%PACKAGES_DIR%" mkdir "%PACKAGES_DIR%"

echo.
echo 1. 下载便携Python...
if not exist "%PYTHON_DIR%\python.exe" (
    echo 正在下载Python便携版...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-win32.zip' -OutFile '%PACKAGES_DIR%\python.zip'}"
    if exist "%PACKAGES_DIR%\python.zip" (
        echo 正在解压Python...
        powershell -Command "& {Expand-Archive -Path '%PACKAGES_DIR%\python.zip' -DestinationPath '%PYTHON_DIR%'}"
        del "%PACKAGES_DIR%\python.zip"
        echo Python便携版下载完成！
    ) else (
        echo 下载失败，请手动下载Python便携版到: %PACKAGES_DIR%
        echo 下载地址: https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-win32.zip
        pause
        exit /b 1
    )
) else (
    echo Python便携版已存在
)

echo.
echo 2. 配置Python环境...

REM 创建pip配置
echo 正在配置pip...
(
echo [global]^
echo target = %~dp0python\Lib\site-packages^
echo python = %~dp0python\python.exe^
echo [install]^
echo prefix = %~dp0python^
echo [packaging]^
echo use-system-site-packages = false
) > "%PYTHON_DIR%\pip.ini"

REM 修改python路径
echo import site > "%PYTHON_DIR%\python311._pth"
echo import sys >> "%PYTHON_DIR%\python311._pth"
echo sys.path.insert^^(0, '^^%~dp0python\Lib/site-packages'^) >> "%PYTHON_DIR%\python311._pth"

echo.
echo 3. 下载依赖包...

REM 使用系统Python下载包（如果没有就安装）
echo 正在下载所需的依赖包...
cd /d "%PACKAGES_DIR%"

REM 下载whl文件
echo 下载Pillow...
python -m pip download --no-binary=:all: --platform win32 --python-version 311 --only-binary=:all: Pillow
echo 下载pynput...
python -m pip download --no-binary=:all: --platform win32 --python-version 311 --only-binary=:all: pynput
echo 下载psutil...
python -m pip download --no-binary=:all: --platform win32 --python-version 311 --only-binary=:all: psutil

REM 安装到便携环境
echo 正在安装到便携环境...
"%PYTHON_DIR%\python.exe" -m pip install --no-index --find-links="%PACKAGES_DIR%" Pillow pynput psutil

echo.
echo 4. 复制脚本文件...

REM 复制脚本文件
copy "%PROJECT_DIR%yuanshen_monitor.py" "%PORTABLE_DIR%\" > nul
copy "%PROJECT_DIR%__init__.py" "%PORTABLE_DIR%\" > nul
copy "%PROJECT_DIR%管理员启动.py" "%PORTABLE_DIR%\" > nul
copy "%PROJECT_DIR%requirements.txt" "%PORTABLE_DIR%\" > nul

REM 创建便携启动脚本
(
echo @echo off
echo title YuanShen 自动按键监听器
echo cd /d "%%~dp0"
echo set PYTHONPATH=%%~dp0python;%%~dp0python\Lib;%%~dp0python\Lib\site-packages
echo set PATH=%%~dp0python;%%PATH%%
echo echo 正在启动监听器...
echo python yuanshen_monitor.py
echo pause
) > "%PORTABLE_DIR%\启动监听器.bat"

REM 创建管理员启动脚本
(
echo @echo off
echo cd /d "%%~dp0"
echo set PYTHONPATH=%%~dp0python;%%~dp0python\Lib;%%~dp0python\Lib\site-packages
echo set PATH=%%~dp0python;%%PATH%%
echo echo 正在启动自动按键脚本...
echo python 管理员启动.py --mode 1
echo pause
) > "%PORTABLE_DIR%\管理员模式启动.bat"

REM 创建说明文件
(
echo YuanShen 自动按键工具 - 便携版
echo =============================================
echo.
echo 文件说明：
echo - python/          : 便携Python环境
echo - 启动监听器.bat  : 主程序入口
echo - 管理员模式启动.bat : 手动启动按键脚本
echo.
echo 使用方法：
echo 1. 双击 "启动监听器.bat"
echo 2. 启动原神游戏
echo 3. 游戏中使用鼠标侧键控制按键
echo 4. 关闭游戏会自动停止脚本
echo.
echo 特性：
echo - 无需安装Python
echo - 无需安装依赖包
echo - 纯绿色便携
echo - 自动管理员权限
echo.
echo 注意事项：
echo - 首次运行请确认UAC权限
echo - 防火墙/杀毒软件可能需要放行
) > "%PORTABLE_DIR%\使用说明.txt"

echo.
echo === 便携环境创建完成 ===
echo.
echo 便携版位置: %PORTABLE_DIR%
echo.
echo 使用方法：
echo 1. 将整个 "便携版" 文件夹复制到目标电脑
echo 2. 双击 "启动监听器.bat" 即可使用
echo.
echo 按任意键退出...
pause > nul