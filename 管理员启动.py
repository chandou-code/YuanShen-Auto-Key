import os
import ctypes
from ctypes import wintypes
import sys
import argparse

def run_python_as_admin(script_path, args=None):
    """以管理员权限运行Python脚本"""
    # 确保路径是绝对路径
    script_abs_path = os.path.abspath(script_path)

    # 检查文件是否存在
    if not os.path.exists(script_abs_path):
        print(f"错误：未找到脚本文件 - {script_abs_path}")
        return False

    # 构建命令行参数
    if args:
        cmd_args = f'"{sys.executable}" "{script_abs_path}" {" ".join(args)}'
    else:
        cmd_args = f'"{sys.executable}" "{script_abs_path}"'

    # 调用Windows API以管理员权限运行程序
    shell32 = ctypes.WinDLL("shell32", use_last_error=True)

    # 定义函数参数类型
    shell32.ShellExecuteW.argtypes = (
        wintypes.HWND,  # hwnd
        wintypes.LPCWSTR,  # lpOperation
        wintypes.LPCWSTR,  # lpFile
        wintypes.LPCWSTR,  # lpParameters
        wintypes.LPCWSTR,  # lpDirectory
        ctypes.c_int  # nShowCmd
    )
    shell32.ShellExecuteW.restype = wintypes.HINSTANCE

    # 执行命令：以管理员权限运行Python脚本
    result = shell32.ShellExecuteW(
        None,  # 无父窗口
        "runas",  # 操作：以管理员权限运行
        sys.executable,  # Python解释器
        f'"{script_abs_path}" {" ".join(args) if args else ""}',  # 脚本路径和参数
        os.path.dirname(script_abs_path),  # 工作目录
        1  # 显示窗口（SW_SHOWNORMAL）
    )

    # 检查执行结果（返回值大于32表示成功）
    if result <= 32:
        print(f"启动失败，错误代码：{result}")
        print("可能的原因：权限不足或文件无法访问")
        return False
    else:
        print(f"已成功请求管理员权限启动：{script_abs_path}")
        return True


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='以管理员权限启动自动按键脚本')
    parser.add_argument('--mode', type=str, choices=['1', '2'], 
                       help='启动模式: 1=空格+F模式, 2=长按右键模式')
    args = parser.parse_args()
    
    # 构建要传递给目标脚本的参数
    script_args = []
    if args.mode:
        script_args.extend(['--mode', args.mode])
    
    # 运行脚本
    script_name = "__init__.py"
    success = run_python_as_admin(script_name, script_args)
    
    if not success:
        input("按回车键退出...")
        sys.exit(1)