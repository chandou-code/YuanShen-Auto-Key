# YuanShen Auto Key - 原神自动按键工具

<div align="center">

![原神](https://img.shields.io/badge/游戏-原神-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![Windows](https://img.shields.io/badge/平台-Windows-lightgrey)
![License](https://img.shields.io/badge/许可证-MIT-orange)

[![便携版](https://img.shields.io/badge/版本-便携版1.0-brightgreen)](#-便携版)
[![自动监听](https://img.shields.io/badge/功能-自动监听-success)](#-主要功能)

</div>

## 🎮 项目简介

YuanShen Auto Key 是一个专为原神游戏设计的自动化按键工具。它能够自动监听原神游戏的启动和关闭，并在游戏运行时提供自动按键跳过剧情功能，帮助玩家简化重复性操作。

## ✨ 主要功能

### 🔄 智能进程监听
- **自动检测游戏启动**：当检测到 YuanShen.exe 进程启动时，自动启动自动按键脚本
- **自动关闭脚本**：当游戏关闭时，自动停止按键脚本
- **实时状态显示**：显示当前监听状态和脚本运行状态

### 🎯 自动按键模式
- **空格+F模式**（默认）：模拟连续的空格和F按键操作
- **长按右键模式**：持续按住鼠标右键
- **鼠标侧键控制**：使用鼠标侧键（前进/后退键）控制按键的开始/停止

### 🛡️ 权限管理
- **自动管理员权限**：自动请求必要的管理员权限
- **安全权限处理**：优雅处理权限提升过程

### 🎨 用户界面
- **实时通知**：显示脚本启动/停止的通知弹窗
- **状态指示器**：彩色图标显示当前状态
- **中文界面**：完全中文化的用户界面

## 🚀 快速开始

### 📦 便携版（推荐）

1. **下载便携版**
   ```bash
   # 克隆项目
   git clone https://github.com/your-username/yuanshen-auto-key.git
   cd yuanshen-auto-key
   
   # 运行一键便携版创建器
   一键便携版.bat
   ```

2. **使用便携版**
   - 将生成的 `YuanShenAutoKey` 文件夹复制到目标电脑
   - 双击 `启动监听器.bat`
   - 启动原神游戏即可自动开始

### 🔧 开发版

如果你已有Python环境：

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/yuanshen-auto-key.git
   cd yuanshen-auto-key
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   # 方式1：使用批处理文件
   监听YuanShen启动.bat
   
   # 方式2：直接运行Python脚本
   python yuanshen_monitor.py
   ```

## 📋 系统要求

- **操作系统**：Windows 7 或更高版本
- **Python版本**：3.11+（开发版）
- **管理员权限**：需要（用于模拟按键）
- **网络连接**：首次创建便携版时需要

## 🎯 使用方法

### 基本使用流程

1. **启动监听器**：运行 `启动监听器.bat`
2. **启动游戏**：正常启动原神游戏
3. **自动按键**：
   - 游戏启动后自动开始空格+F按键
   - 使用鼠标侧键控制按键的开始/停止
4. **关闭游戏**：关闭原神后脚本自动停止

### 鼠标侧键控制

| 按键 | 功能 |
|------|------|
| 鼠标侧键1/2 | 切换自动按键开启/关闭 |
| ESC键 | 完全退出脚本 |

### 模式切换

如果你需要手动选择模式：

```bash
# 空格+F模式
python __init__.py --mode 1

# 长按右键模式  
python __init__.py --mode 2
```

## 📁 项目结构

```
空格F/
├── README.md                    # 项目说明文件
├── requirements.txt             # Python依赖列表
├── 使用说明.txt               # 详细使用说明
├── 打包说明.md               # 便携版制作指南
│
├── 核心脚本/
│   ├── __init__.py            # 主自动按键脚本
│   ├── yuanshen_monitor.py   # 进程监听器
│   ├── 管理员启动.py        # 管理员权限启动器
│   └── build_exe.py          # PyInstaller打包脚本
│
├── 启动脚本/
│   ├── 监听YuanShen启动.bat    # 主监听器启动器
│   ├── 空格F.bat           # 传统启动器
│   ├── 空格F启动.bat        # 管理员启动器
│   ├── 创建便携环境.bat      # 便携环境创建器
│   └── 一键便携版.bat       # 一键便携版创建器
│
└── 便携版/                  # 生成的便携版目录
    ├── python/               # 内置Python环境
    ├── 启动监听器.bat       # 便携版启动器
    └── 使用说明.txt         # 便携版说明
```

## 🛠️ 技术实现

### 核心技术栈
- **语言**：Python 3.11+
- **GUI框架**：Tkinter（标准库）
- **图像处理**：PIL/Pillow
- **输入模拟**：Pynput
- **进程管理**：Psutil
- **系统API**：ctypes（Windows API）

### 关键特性

#### 🔄 进程监听机制
```python
def check_yuanshen_process(self):
    """检查 YuanShen.exe 进程是否存在"""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == 'yuanshen.exe':
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False, None
```

#### 🎯 按键模拟
```python
def auto_space_f(self):
    """空格+F模式 - 连续模拟空格和F按键"""
    controller = keyboard.Controller()
    while self.running and self.active:
        controller.press(' ')
        time.sleep(0.05)
        controller.release(' ')
        time.sleep(0.1)
        
        controller.press('f')
        time.sleep(0.05)
        controller.release('f')
```

#### 🛡️ 管理员权限提升
```python
def run_python_as_admin(script_path, args=None):
    """以管理员权限运行Python脚本"""
    shell32 = ctypes.WinDLL("shell32", use_last_error=True)
    result = shell32.ShellExecuteW(
        None, "runas", sys.executable, 
        f'"{script_abs_path}" {" ".join(args) if args else ""}',
        os.path.dirname(script_abs_path), 1
    )
```

## 🔧 配置选项

### 自定义配置

你可以修改以下参数来自定义行为：

```python
# 在 yuanshen_monitor.py 中修改
class YuanShenProcessMonitor:
    def __init__(self):
        self.check_interval = 2.0  # 进程检查间隔（秒）
        self.process_name = "yuanshen.exe"  # 监听的进程名

# 在 __init__.py 中修改按键间隔
def auto_space_f(self):
    time.sleep(0.05)  # 按键按下持续时间
    time.sleep(0.1)   # 按键间隔时间
```

## 📝 更新日志

### v1.0.0 (2024-11-17)
- ✨ 初始版本发布
- 🔄 自动进程监听功能
- 🎯 空格+F自动按键模式
- 🛡️ 管理员权限自动获取
- 📦 完整便携版支持
- 🎨 实时通知界面

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. **Fork** 本项目
2. **创建功能分支** (`git checkout -b feature/AmazingFeature`)
3. **提交更改** (`git commit -m 'Add some AmazingFeature'`)
4. **推送分支** (`git push origin feature/AmazingFeature`)
5. **创建Pull Request**

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/your-username/yuanshen-auto-key.git
cd yuanshen-auto-key

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
python yuanshen_monitor.py
```

## ❓ 常见问题

### Q: 提示"无法找到 YuanShen.exe 进程"？
A: 确保原神游戏正在运行，且进程名为 "YuanShen.exe"

### Q: 按键没有反应？
A: 确保以管理员权限运行，并关闭其他可能冲突的按键工具

### Q: 便携版下载失败？
A: 检查网络连接，或手动下载Python便携版

### Q: 杀毒软件报毒？
A: 添加到杀毒软件白名单，这是误报

### Q: 如何切换到长按右键模式？
A: 使用命令行参数 `python __init__.py --mode 2`

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

本工具仅供学习和研究使用。请遵守游戏的服务条款，不要在多人模式中使用自动化工具。使用本工具所产生的任何后果由用户自行承担。

## 🙏 致谢

- [Pynput](https://github.com/moses-palmer/pynput) - 强大的输入模拟库
- [Psutil](https://github.com/giampaolo/psutil) - 跨平台进程和系统监控库
- [Pillow](https://github.com/python-pillow/Pillow) - Python图像处理库
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Python标准GUI库

---

<div align="center">

**🌟 如果这个项目对你有帮助，请给个Star！**

[](https://star-history.com/#chandou-code/YuanShen-Auto-Key)


</div>
