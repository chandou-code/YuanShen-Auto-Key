import os
import ctypes
from ctypes import wintypes


def run_bat_as_admin(bat_path):
    # 确保路径是绝对路径
    bat_abs_path = os.path.abspath(bat_path)

    # 检查文件是否存在
    if not os.path.exists(bat_abs_path):
        print(f"错误：未找到批处理文件 - {bat_abs_path}")
        return False

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

    # 执行命令：以管理员权限运行批处理文件
    result = shell32.ShellExecuteW(
        None,  # 无父窗口
        "runas",  # 操作：以管理员权限运行
        bat_abs_path,  # 要运行的批处理文件路径
        None,  # 无额外参数
        os.path.dirname(bat_abs_path),  # 工作目录
        1  # 显示窗口（SW_SHOWNORMAL）
    )

    # 检查执行结果（返回值大于32表示成功）
    if result <= 32:
        print(f"启动失败，错误代码：{result}")
        print("可能的原因：权限不足或文件无法访问")
        return False
    else:
        print(f"已成功请求管理员权限启动：{bat_abs_path}")
        return True


if __name__ == "__main__":
    # 要运行的批处理文件名（如果带空格需完整名称，例如" 空格F.bat"）
    bat_filename = "空格F.bat"  # 如果实际文件名包含空格，修改为对应的名称即可
    run_bat_as_admin(bat_filename)
