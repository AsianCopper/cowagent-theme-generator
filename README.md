# 🎸 CowAgent 主题生成器

一个可视化的 CowAgent 主题生成工具，根据你喜欢的壁纸自动生成适配的白天/夜晚主题。

## ✨ 功能特性

- 🎨 **智能取色** - 自动从壁纸中提取主色调
- 🌅 **双模式适配** - 自动生成白天和夜晚两套配色方案
- 🖌️ **一体化设计** - 侧边栏和聊天区域颜色自动协调
- 🚀 **一键安装** - 自动安装到 CowAgent，自动备份原文件
- 🎥 **实时预览** - 生成前可预览颜色搭配

## 📖 使用方法

### 方法一：使用预编译的 EXE 文件（推荐）

1. 下载 `CowAgent-ThemeGenerator.exe`
2. 双击运行
3. 点击"选择壁纸"上传你喜欢的图片
4. 点击"生成主题"
5. 点击"安装到 CowAgent"

### 方法二：从源码运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python theme_generator.py
```

### 方法三：自己打包 EXE

```bash
# 运行打包脚本
build_exe.bat
```

## 🖼️ 工作原理

1. **图片分析** - 使用 PIL 库分析壁纸图片的颜色分布
2. **主色提取** - 通过颜色聚类算法提取主色调
3. **颜色计算** - 根据主色调生成亮暗两套配色方案
4. **样式生成** - 自动生成 CSS 和 HTML 文件
5. **自动安装** - 将文件复制到 CowAgent 目录，自动备份原文件

## 📁 文件结构

```
cow-theme-generator/
├── theme_generator.py    # 主程序
├── requirements.txt      # Python 依赖
├── build_exe.bat          # 打包脚本
└── README.md              # 说明文档
```

## 🎭 生成的主题文件

生成的主题包含以下文件：

- `chat.html` - 主页面 HTML
- `custom-theme.css` - 自定义样式
- `chat-bg.jpg` - 背景图片

## 📝 备注

- 支持的图片格式：PNG, JPG, JPEG, BMP, GIF
- 建议使用高清壁纸以获得最佳效果
- 原始文件会自动备份到 `custom_backup/` 目录

## 💝 致谢

By: 亚洲铜 x BocchiBot

特别感谢 CowAgent 项目: https://github.com/zhayujie/CowAgent
