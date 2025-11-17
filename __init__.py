import threading
import time
import tkinter as tk
import os
import platform
import queue
from pynput import mouse, keyboard  # 使用 pynput 替代 keyboard 库
import sys
import argparse
import warnings

# 抑制PIL的libpng警告
warnings.filterwarnings("ignore", category=UserWarning, message=".*iCCP.*")

# 延迟导入PIL以减少启动时的警告
Image = None
ImageDraw = None  
ImageTk = None

def get_pil_modules():
    """延迟导入PIL模块"""
    global Image, ImageDraw, ImageTk
    if Image is None:
        from PIL import Image, ImageDraw, ImageTk
    return Image, ImageDraw, ImageTk


class NotificationWindow:
    def __init__(self):
        self.window = None
        self.label = None
        self.active_icon = None
        self.inactive_icon = None
        self.icons_created = False
        self.task_queue = queue.Queue()
        self.ui_thread = None

        # 检测操作系统并设置合适的字体
        self.os_name = platform.system()
        if self.os_name == "Windows":
            self.font_title = ("Microsoft YaHei", 10, "bold")
            self.font_status = ("Microsoft YaHei", 14, "bold")
        elif self.os_name == "Darwin":  # macOS
            self.font_title = ("PingFang SC", 10, "bold")
            self.font_status = ("PingFang SC", 14, "bold")
        else:  # Linux或其他系统
            self.font_title = ("Sans", 10, "bold")
            self.font_status = ("Sans", 14, "bold")

        # 启动UI线程
        self.start_ui_thread()

    def start_ui_thread(self):
        """启动UI线程"""
        self.ui_thread = threading.Thread(target=self.ui_mainloop, daemon=True)
        self.ui_thread.start()

    def ui_mainloop(self):
        """UI线程的主循环"""
        # 创建隐藏的主窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口

        while True:
            try:
                # 处理UI任务
                task = self.task_queue.get(timeout=0.1)
                if task[0] == "show":
                    self._show_notification(task[1], task[2])
                elif task[0] == "close":
                    self._close_notification()
            except queue.Empty:
                # 没有任务时继续循环
                pass
            except Exception as e:
                print(f"UI线程错误: {e}")

            # 更新UI
            root.update_idletasks()
            root.update()

    def create_icons(self):
        """创建图标资源"""
        if self.icons_created:
            return

        try:
            # 创建简单的图标
            self.active_icon = self.create_icon("green")
            self.inactive_icon = self.create_icon("red")
            self.icons_created = True
        except Exception as e:
            print(f"图标创建失败: {e}")
            self.active_icon = None
            self.inactive_icon = None

    def create_icon(self, color):
        """创建简单的圆形图标"""
        Image, ImageDraw, ImageTk = get_pil_modules()
        size = 32
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        if color == "green":
            draw.ellipse((0, 0, size - 1, size - 1), fill=(0, 255, 0, 255))
        else:
            draw.ellipse((0, 0, size - 1, size - 1), fill=(255, 0, 0, 255))

        return ImageTk.PhotoImage(img)

    def show(self, active, mode_name):
        """显示通知窗口（线程安全）"""
        # 将任务添加到队列，由UI线程处理
        self.task_queue.put(("show", active, mode_name))

    def _show_notification(self, active, mode_name):
        """实际显示通知窗口（在UI线程中执行）"""
        # 先关闭现有窗口
        self._close_notification()

        try:
            # 创建新窗口
            self.window = tk.Toplevel()
            self.window.overrideredirect(True)
            self.window.attributes("-topmost", True)
            self.window.attributes("-alpha", 0.9)

            # 设置窗口位置（右下角）
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            window_width = 220
            window_height = 70
            x = screen_width - window_width - 20
            y = screen_height - window_height - 50

            self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

            # 设置背景色
            bg_color = "#2c3e50"
            self.window.configure(bg=bg_color)

            # 创建内容框架
            frame = tk.Frame(self.window, bg=bg_color)
            frame.pack(fill="both", expand=True, padx=10, pady=10)

            # 创建图标
            self.create_icons()

            # 添加图标
            if self.active_icon and self.inactive_icon:
                icon_label = tk.Label(frame, image=self.active_icon if active else self.inactive_icon, bg=bg_color)
                icon_label.grid(row=0, column=0, rowspan=2, padx=(0, 10), sticky="n")

            # 添加标题
            title = tk.Label(frame, text="自动按键状态", fg="white", bg=bg_color, font=self.font_title)
            title.grid(row=0, column=1, sticky="w")

            # 添加状态文本
            status_text = "已启用" if active else "已停止"
            status_color = "#2ecc71" if active else "#e74c3c"
            self.label = tk.Label(frame, text=f"{status_text} ({mode_name})", fg=status_color, bg=bg_color,
                                  font=self.font_status)
            self.label.grid(row=1, column=1, sticky="w")

            # 添加关闭按钮
            close_btn = tk.Button(frame, text="×", command=self.close,
                                  bg="#e74c3c", fg="white", bd=0, font=("Arial", 8),
                                  width=2, height=1)
            close_btn.grid(row=0, column=2, rowspan=2, padx=(10, 0), sticky="ne")

            # 自动关闭窗口
            self.window.after(3000, self.close)

            # 显示窗口
            self.window.deiconify()
        except Exception as e:
            print(f"创建通知窗口时出错: {e}")
            self.window = None

    def close(self):
        """关闭通知窗口（线程安全）"""
        self.task_queue.put(("close", None))

    def _close_notification(self):
        """实际关闭通知窗口（在UI线程中执行）"""
        if self.window:
            try:
                self.window.destroy()
                self.window = None
            except Exception as e:
                print(f"关闭通知窗口时出错: {e}")
                self.window = None


class AutoKeyPresser:
    def __init__(self):
        self.running = False
        self.active = False
        self.thread = None
        self.notification = NotificationWindow()
        self.mouse_listener = None
        self.keyboard_listener = None
        self.mode = None  # 存储当前选择的模式
        self.mouse_controller = mouse.Controller()  # 用于模拟鼠标操作

    def start(self):
        """启动程序"""
        self.running = True

        # 如果没有预设模式，显示主菜单
        if not self.mode:
            self.show_main_menu()

        # 如果用户选择了模式，启动监听器
        if self.mode:
            print(f"程序已启动。按下鼠标侧键(通常为按钮4或5)开始/停止自动按键（模式: {self.mode}）")

            # 创建并启动鼠标监听器
            self.mouse_listener = mouse.Listener(on_click=self.on_click)
            self.mouse_listener.daemon = True
            self.mouse_listener.start()

            

            # 主线程等待退出信号
            try:
                while self.running:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.stop()
        else:
            print("未选择模式，程序退出。")

    def show_main_menu(self):
        """显示主菜单让用户选择模式"""
        print("\n" + "=" * 40)
        print("自动按键工具")
        print("=" * 40)
        print("请选择模式:")
        print("1. 空格+F模式（快速按键）")
        print("2. 长按右键模式（持续按住右键）")
        print("3. 退出程序")

        while True:
            choice = input("\n请输入选项数字 (1-3): ").strip()

            if choice == "1":
                self.mode = "空格+F模式"
                break
            elif choice == "2":
                self.mode = "长按右键模式"
                break
            elif choice == "3":
                print("退出程序。")
                self.running = False
                return
            else:
                print("无效输入，请重新选择。")

    def stop(self):
        """停止程序"""
        self.running = False
        self.active = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print("\n程序已停止。")

    def on_press(self, key):
        """键盘按键事件处理"""
        try:
            if key == keyboard.Key.esc:
                self.stop()
                return False  # 停止监听器
        except AttributeError:
            pass

    def on_click(self, x, y, button, pressed):
        """鼠标点击事件处理"""
        if pressed:
            if button in [mouse.Button.x1, mouse.Button.x2]:  # 仅检测侧键
                self.toggle_auto_press()

    def toggle_auto_press(self):
        """切换自动按键状态"""
        self.active = not self.active

        if self.active:
            print(f"\n自动按键已启动 ({self.mode})。按下鼠标侧键停止。")
            # 显示通知
            self.notification.show(True, self.mode)
            # 创建并启动自动按键线程
            auto_thread = threading.Thread(target=self.auto_press)
            auto_thread.daemon = True
            auto_thread.start()
        else:
            print(f"\n自动按键已停止 ({self.mode})。")
            # 显示通知
            self.notification.show(False, self.mode)

    def auto_press(self):
        """根据选择的模式执行不同的按键操作"""
        if self.mode == "空格+F模式":
            self.auto_space_f()
        elif self.mode == "长按右键模式":
            self.auto_right_click()

    def auto_space_f(self):
        """空格+F模式"""
        controller = keyboard.Controller()
        while self.running and self.active:  # 双重检查
            controller.press(' ')
            time.sleep(0.05)
            controller.release(' ')
            time.sleep(0.1)

            controller.press('f')
            time.sleep(0.05)
            controller.release('f')

            # 更频繁的状态检查
            for _ in range(5):
                if not self.active:
                    return
                time.sleep(0.1)

    def auto_right_click(self):
        """长按右键模式"""
        while self.running and self.active:
            # 按下右键
            self.mouse_controller.press(mouse.Button.right)

            # 保持按下状态，直到停止
            while self.active and self.running:
                time.sleep(0.1)

            # 释放右键
            self.mouse_controller.release(mouse.Button.right)


if __name__ == "__main__":
    # 添加命令行参数解析
    parser = argparse.ArgumentParser(description='自动按键工具')
    parser.add_argument('--mode', type=str, choices=['1', '2'], 
                       help='启动模式: 1=空格+F模式, 2=长按右键模式')
    args = parser.parse_args()
    
    presser = AutoKeyPresser()
    
    # 如果通过命令行指定了模式，直接设置
    if args.mode:
        if args.mode == '1':
            presser.mode = "空格+F模式"
        elif args.mode == '2':
            presser.mode = "长按右键模式"
    
    presser.start()
