@echo off
chcp 65001 > nul
title YuanShen 自动按键工具 - 一键便携版

echo ================================================
echo    YuanShen 自动按键工具 - 一键便携版创建器
echo ================================================
echo.

set "WORK_DIR=%~dp0"
set "PORTABLE_DIR=%WORK_DIR%YuanShenAutoKey"

echo 正在创建便携版目录...
if exist "%PORTABLE_DIR%" rmdir /s /q "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%"

echo.
echo [1/6] 正在下载便携Python环境...
echo 正在下载，请稍候...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-win32.zip' -OutFile '%PORTABLE_DIR%\python.zip'}"

if not exist "%PORTABLE_DIR%\python.zip" (
    echo 下载失败！请检查网络连接
    pause
    exit /b 1
)

echo 正在解压Python...
powershell -Command "Expand-Archive -Path '%PORTABLE_DIR%\python.zip' -DestinationPath '%PORTABLE_DIR%\python'"
del "%PORTABLE_DIR%\python.zip"

echo.
echo [2/6] 正在配置Python环境...
REM 修改pth文件以启用site-packages
echo import site > "%PORTABLE_DIR%\python\python311._pth"
echo import sys >> "%PORTABLE_DIR%\python\python311._pth"
echo sys.path.insert^(0, 'Lib/site-packages'^) >> "%PORTABLE_DIR%\python\python311._pth"

REM 获取pip
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%PORTABLE_DIR%\get-pip.py'}"

echo.
echo [3/6] 正在安装pip...
"%PORTABLE_DIR%\python\python.exe" "%PORTABLE_DIR%\get-pip.py" --no-warn-script-location
del "%PORTABLE_DIR%\get-pip.py"

echo.
echo [4/6] 正在安装依赖包...
"%PORTABLE_DIR%\python\python.exe" -m pip install --no-warn-script-location Pillow pynput psutil

echo.
echo [5/6] 正在复制脚本文件...

REM 复制和创建所需的文件
copy "%WORK_DIR%yuanshen_monitor.py" "%PORTABLE_DIR%\" > nul
copy "%WORK_DIR%__init__.py" "%PORTABLE_DIR%\" > nul
copy "%WORK_DIR%管理员启动.py" "%PORTABLE_DIR%\" > nul

REM 创建启动批处理
(
echo @echo off
echo title YuanShen 自动按键监听器
echo cd /d "%%~dp0"
echo set PATH=%%~dp0python;%%PATH%%
echo echo 正在启动监听器...
echo echo 使用说明：
echo echo 1. 启动原神会自动开始空格+F按键
echo echo 2. 使用鼠标侧键控制按键开关
echo echo 3. 关闭原神会自动停止按键
echo echo.
echo echo 按任意键开始监听...
echo pause ^> nul
echo python yuanshen_monitor.py
echo echo.
echo echo 监听器已退出
echo pause
) > "%PORTABLE_DIR%\启动监听器.bat"

REM 创建管理员模式启动器
(
echo @echo off
echo cd /d "%%~dp0"
echo set PATH=%%~dp0python;%%PATH%%
echo echo 正在启动管理员模式按键脚本...
echo python 管理员启动.py --mode 1
echo pause
) > "%PORTABLE_DIR%\管理员模式.bat"

REM 创建使用说明
(
echo YuanShen 自动按键工具 - 便携版
echo ====================================
echo.
echo 文件说明：
echo - python/          : 内置Python环境（约25MB）
echo - 启动监听器.bat  : 主程序（推荐使用）
echo - 管理员模式.bat   : 手动启动按键脚本
echo.
echo 使用步骤：
echo 1. 双击 "启动监听器.bat"
echo 2. 启动原神游戏
echo 3. 游戏中使用鼠标侧键控制按键
echo 4. 关闭游戏自动停止
echo.
echo 特性：
echo - 完全便携，无需安装Python
echo - 自动下载所有依赖
echo - 支持管理员权限
echo - 自动进程监听
echo.
echo 注意事项：
echo - 首次使用会弹出UAC，请点击"是"
echo - 杀毒软件可能需要添加信任
echo.
echo 版本：便携版 v1.0
echo 大小：约30MB
) > "%PORTABLE_DIR%\使用说明.txt"

echo.
echo [6/6] 正在清理临时文件...
if exist "%PORTABLE_DIR%\python\*.chm" del "%PORTABLE_DIR%\python\*.chm"

echo.
echo ================================================
echo              创建完成！
echo ================================================
echo.
echo 便携版已创建在: %PORTABLE_DIR%
echo 大小: 约30MB
echo.
echo 使用方法：
echo 1. 将整个 "YuanShenAutoKey" 文件夹复制到目标电脑
echo 2. 双击 "启动监听器.bat" 即可使用
echo.
echo 是否打开便携版文件夹？^(Y/N^)
set /p choice=请选择: 
if /i "%choice%"=="Y" start "" "%PORTABLE_DIR%"

echo.
echo 按任意键退出...
pause > nul