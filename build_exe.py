#!/usr/bin/env python3
"""
打包脚本 - 将项目打包成独立的可执行文件
需要先安装: pip install pyinstaller
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def install_pyinstaller():
    """安装pyinstaller"""
    try:
        import pyinstaller
        print("PyInstaller 已安装")
        return True
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def build_main_script():
    """打包主监听脚本"""
    print("正在打包主监听脚本...")
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个exe
        "--windowed",                   # 不显示控制台窗口（可选）
        "--name=YuanShenMonitor",       # exe文件名
        "--icon=icon.ico",              # 图标文件（如果有的话）
        "--add-data=管理员启动.py;.",    # 添加额外文件
        "--add-data=__init__.py;.",      # 添加额外文件
        "--add-data=requirements.txt;.", # 添加额外文件
        "--hidden-import=PIL.Image",      # 隐藏导入
        "--hidden-import=PIL.ImageDraw",
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=pynput",
        "--hidden-import=psutil",
        "yuanshen_monitor.py"
    ]
    
    # 如果没有图标文件，移除图标参数
    if not Path("icon.ico").exists():
        cmd = [arg for arg in cmd if arg != "--icon=icon.ico"]
    
    try:
        subprocess.run(cmd, check=True)
        print("主监听脚本打包完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        return False

def build_auto_key_script():
    """打包自动按键脚本"""
    print("正在打包自动按键脚本...")
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个exe
        "--windowed",                   # 不显示控制台窗口
        "--name=AutoKeyPresser",         # exe文件名
        "--icon=icon.ico",              # 图标文件（如果有的话）
        "--hidden-import=PIL.Image",      # 隐藏导入
        "--hidden-import=PIL.ImageDraw", 
        "--hidden-import=PIL.ImageTk",
        "--hidden-import=pynput",
        "--hidden-import=tkinter",
        "__init__.py"
    ]
    
    # 如果没有图标文件，移除图标参数
    if not Path("icon.ico").exists():
        cmd = [arg for arg in cmd if arg != "--icon=icon.ico"]
    
    try:
        subprocess.run(cmd, check=True)
        print("自动按键脚本打包完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"打包失败: {e}")
        return False

def create_portable_package():
    """创建便携式包"""
    print("正在创建便携式包...")
    
    portable_dir = Path("便携版")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir()
    
    # 复制打包好的exe文件
    dist_dir = Path("dist")
    if dist_dir.exists():
        for exe_file in dist_dir.glob("*.exe"):
            shutil.copy2(exe_file, portable_dir)
    
    # 创建启动脚本
    start_bat = portable_dir / "启动监听器.bat"
    start_bat.write_text("""@echo off
title YuanShen 自动按键监听器
echo 正在启动 YuanShen.exe 监听器...
echo.
echo 使用说明：
echo 1. 启动原神游戏会自动启动空格+F按键脚本
echo 2. 关闭原神游戏会自动停止按键脚本
echo 3. 游戏中使用鼠标侧键控制按键开始/停止
echo.
echo 按任意键启动监听器...
pause > nul

YuanShenMonitor.exe

echo.
echo 监听器已退出，按任意键关闭窗口...
pause > nul
""")
    
    # 创建管理员启动脚本（备用）
    admin_bat = portable_dir / "管理员模式启动.bat"
    admin_bat.write_text("""@echo off
title AutoKeyPresser (管理员模式)
echo 正在启动自动按键脚本...
echo.
echo 此脚本将以空格+F模式启动
echo 使用鼠标侧键控制按键的开始/停止
echo.
echo 按任意键启动...
pause > nul

AutoKeyPresser.exe

echo.
echo 脚本已退出，按任意键关闭窗口...
pause > nul
""")
    
    # 创建说明文件
    readme_txt = portable_dir / "使用说明.txt"
    readme_txt.write_text("""YuanShen 自动按键工具 - 便携版
================================

文件说明：
- YuanShenMonitor.exe  : 主监听器，监听游戏启动/关闭
- AutoKeyPresser.exe    : 自动按键脚本（备用）
- 启动监听器.bat        : 一键启动监听器（推荐使用）

使用方法：
1. 双击 "启动监听器.bat"
2. 启动原神游戏（监听器会自动启动按键脚本）
3. 游戏中使用鼠标侧键控制自动按键的开始/停止
4. 关闭游戏后监听器会自动停止按键脚本

特性：
- ✅ 无需安装Python和依赖包
- ✅ 自动获取管理员权限
- ✅ 自动监听游戏进程
- ✅ 自动启停按键脚本
- ✅ 支持通知提示

注意事项：
- 首次运行可能需要确认UAC权限提示
- 确保杀毒软件不误报
- 如果无法启动，请尝试以管理员身份运行

版本：便携版 1.0
""")
    
    print("便携式包创建完成！")
    print(f"位置: {portable_dir.absolute()}")

def main():
    """主函数"""
    print("=== YuanShen 自动按键工具 - 打包工具 ===")
    print()
    
    # 安装PyInstaller
    if not install_pyinstaller():
        print("安装PyInstaller失败，退出...")
        return
    
    # 清理之前的构建
    for cleanup_dir in ["build", "dist", "便携版"]:
        if Path(cleanup_dir).exists():
            shutil.rmtree(cleanup_dir)
            print(f"清理旧的 {cleanup_dir} 目录")
    
    # 打包脚本
    if build_main_script() and build_auto_key_script():
        # 创建便携式包
        create_portable_package()
        
        print()
        print("=== 打包完成 ===")
        print("便携版已创建在 '便携版' 文件夹中")
        print("可以将整个文件夹复制到任何电脑上使用")
        print()
    else:
        print("打包失败！")

if __name__ == "__main__":
    main()