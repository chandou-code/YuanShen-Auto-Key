import os
import time
import psutil
import subprocess
import signal
import sys
from pathlib import Path

class YuanShenProcessMonitor:
    def __init__(self):
        self.script_process = None
        self.project_dir = Path(__file__).parent
        self.running = True
        self.check_interval = 2.0  # 检查间隔（秒）
    
    def check_yuanshen_process(self):
        """检查 YuanShen.exe 进程是否存在"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == 'yuanshen.exe':
                    return True, proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return False, None
    
    def start_auto_press_script(self):
        """启动自动按键脚本并自动选择空格+F模式"""
        try:
            # 使用管理员权限启动脚本
            admin_script_path = self.project_dir / '管理员启动.py'
            
            if admin_script_path.exists():
                # 使用管理员权限启动脚本并传递模式参数
                # 注意：这个进程会立即结束，因为它只是请求管理员权限
                launch_process = subprocess.Popen(
                    [sys.executable, str(admin_script_path), '--mode', '1'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=str(self.project_dir),
                    shell=True
                )
                
                # 等待一下让管理员权限脚本完成
                time.sleep(2)
                
                # 查找由我们启动的自动按键脚本进程
                self.script_process = self.find_autopress_process()
            else:
                # 备用方案：直接运行Python脚本
                script_path = self.project_dir / '__init__.py'
                self.script_process = subprocess.Popen(
                    [sys.executable, str(script_path), '--mode', '1'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=str(self.project_dir)
                )
            
            if self.script_process:
                print(f"已启动自动按键脚本 (PID: {self.script_process.pid})，模式: 空格+F")
            else:
                print("已请求启动自动按键脚本，模式: 空格+F")
            print("注意：如果出现UAC提示，请点击'是'以授予管理员权限")
            
        except Exception as e:
            print(f"启动脚本失败: {e}")
    
    def find_autopress_process(self):
        """查找自动按键脚本的进程"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # 检查是否是Python进程
                    if proc.info['name'] == 'python.exe':
                        try:
                            cmdline = proc.cmdline()
                            if cmdline and len(cmdline) > 1 and '__init__.py' in ' '.join(cmdline):
                                return proc
                        except (psutil.AccessDenied, psutil.ZombieProcess):
                            continue
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            print(f"查找进程时出错: {e}")
        return None
    
    def monitor_script_output(self):
        """监听脚本输出"""
        if self.script_process:
            try:
                while self.script_process.poll() is None:
                    line = self.script_process.stdout.readline()
                    if line:
                        print(line.strip())
            except:
                pass
    
    def stop_auto_press_script(self):
        """停止自动按键脚本"""
        try:
            # 如果我们找到了具体进程，停止它
            if self.script_process:
                print(f"正在停止自动按键脚本 (PID: {self.script_process.pid})...")
                
                # 先尝试优雅关闭
                self.script_process.terminate()
                
                # 等待进程结束
                try:
                    self.script_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # 如果进程没有在5秒内结束，强制杀死
                    self.script_process.kill()
                    self.script_process.wait()
                
                print("自动按键脚本已停止")
                self.script_process = None
            
            # 否则，查找并停止所有相关的Python进程
            else:
                print("正在查找并停止自动按键脚本...")
                stopped_count = 0
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        # 检查是否是Python进程
                        if proc.info['name'] == 'python.exe':
                            try:
                                cmdline = proc.cmdline()
                                if cmdline and len(cmdline) > 1 and '__init__.py' in ' '.join(cmdline):
                                    print(f"停止自动按键脚本 (PID: {proc.pid})...")
                                    proc.terminate()
                                    
                                    try:
                                        proc.wait(timeout=3)
                                    except subprocess.TimeoutExpired:
                                        proc.kill()
                                        proc.wait()
                                    
                                    stopped_count += 1
                            except (psutil.AccessDenied, psutil.ZombieProcess):
                                continue
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                
                if stopped_count > 0:
                    print(f"已停止 {stopped_count} 个自动按键脚本")
                else:
                    print("自动按键脚本已停止")
                
        except Exception as e:
            # 权限错误是正常的，因为脚本在管理员权限下运行
            if "AccessDenied" in str(e) or "权限" in str(e):
                print("自动按键脚本已停止（可能需要管理员权限）")
            else:
                print(f"停止脚本时出错: {e}")
        finally:
            self.script_process = None
    
    def monitor_loop(self):
        """主监听循环"""
        print("YuanShen.exe 进程监听器已启动")
        print("正在监听 YuanShen.exe 进程...")
        print("按 Ctrl+C 退出监听器")
        
        was_running = False
        
        try:
            while self.running:
                is_running, pid = self.check_yuanshen_process()
                
                if is_running and not was_running:
                    # 检测到进程启动
                    print(f"检测到 YuanShen.exe 进程启动 (PID: {pid})")
                    print("正在启动自动按键脚本...")
                    self.start_auto_press_script()
                    was_running = True
                    
                elif not is_running and was_running:
                    # 检测到进程关闭
                    print("检测到 YuanShen.exe 进程已关闭")
                    print("正在停止自动按键脚本...")
                    self.stop_auto_press_script()
                    was_running = False
                
                # 等待下次检查
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n收到退出信号，正在停止监听...")
            self.running = False
            self.stop_auto_press_script()
            print("监听器已退出")

def main():
    """主函数"""
    try:
        # 检查是否在Windows系统上运行
        if os.name != 'nt':
            print("此脚本仅支持Windows系统")
            return
        
        # 检查必要的模块
        try:
            import psutil
        except ImportError:
            print("缺少 psutil 模块，正在安装...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            import psutil
        
        # 检查脚本文件是否存在
        script_path = Path(__file__).parent / '__init__.py'
        if not script_path.exists():
            print(f"错误：找不到脚本文件 {script_path}")
            return
        
        # 创建并启动监听器
        monitor = YuanShenProcessMonitor()
        monitor.monitor_loop()
        
    except Exception as e:
        print(f"程序运行出错: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()