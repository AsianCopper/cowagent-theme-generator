#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CowAgent 主题生成器
根据用户上传的壁纸自动生成适配的白天/夜晚主题
"""

import sys
import os
import json
import colorsys
from pathlib import Path
from PIL import Image, ImageStat
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QSlider, QComboBox,
    QProgressBar, QMessageBox, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QColor, QPalette, QFont

class ColorExtractor:
    """从图片中提取颜色"""
    
    @staticmethod
    def get_dominant_color(image_path, num_colors=5):
        """提取图片主色调"""
        with Image.open(image_path) as img:
            # 缩小图片以提高速度
            img = img.convert('RGB')
            img.thumbnail((150, 150))
            
            # 获取颜色直方图
            pixels = list(img.getdata())
            
            # 计算平均颜色
            r_sum = g_sum = b_sum = 0
            for r, g, b in pixels:
                r_sum += r
                g_sum += g
                b_sum += b
            
            total = len(pixels)
            avg_color = (r_sum // total, g_sum // total, b_sum // total)
            
            # 获取主要颜色（通过聚类简化）
            colors = {}
            for r, g, b in pixels:
                # 简化颜色（量化）
                key = (r // 10 * 10, g // 10 * 10, b // 10 * 10)
                colors[key] = colors.get(key, 0) + 1
            
            # 获取最常见的颜色
            sorted_colors = sorted(colors.items(), key=lambda x: x[1], reverse=True)
            dominant_colors = [c[0] for c in sorted_colors[:num_colors]]
            
            return {
                'average': avg_color,
                'dominant': dominant_colors
            }
    
    @staticmethod
    def rgb_to_hex(rgb):
        """RGB 转十六进制"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    
    @staticmethod
    def adjust_brightness(rgb, factor):
        """调整亮度"""
        r, g, b = rgb
        r = min(255, max(0, int(r * factor)))
        g = min(255, max(0, int(g * factor)))
        b = min(255, max(0, int(b * factor)))
        return (r, g, b)
    
    @staticmethod
    def get_contrast_color(rgb):
        """获取对比色（用于文字）"""
        r, g, b = rgb
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        if luminance > 0.5:
            return (30, 30, 30)  # 深色文字
        else:
            return (245, 245, 245)  # 浅色文字

class ThemeGenerator:
    """生成 CowAgent 主题文件"""
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.colors = None
        self.extract_colors()
    
    def extract_colors(self):
        """提取并处理颜色"""
        extractor = ColorExtractor()
        self.colors = extractor.get_dominant_color(self.image_path)
        
        avg = self.colors['average']
        dominant = self.colors['dominant'][0]
        
        # 白天模式颜色（基于主色调，更亮）
        self.light_theme = {
            'sidebar_bg': extractor.adjust_brightness(dominant, 1.3),
            'sidebar_text': extractor.get_contrast_color(extractor.adjust_brightness(dominant, 1.3)),
            'chat_bg': (255, 255, 255),
            'chat_text': (50, 50, 50),
            'accent': dominant,
            'hover': extractor.adjust_brightness(dominant, 1.1),
        }
        
        # 夜晚模式颜色（基于主色调，更暗）
        self.dark_theme = {
            'sidebar_bg': extractor.adjust_brightness(dominant, 0.4),
            'sidebar_text': extractor.get_contrast_color(extractor.adjust_brightness(dominant, 0.4)),
            'chat_bg': (30, 30, 35),
            'chat_text': (220, 220, 220),
            'accent': extractor.adjust_brightness(dominant, 0.8),
            'hover': extractor.adjust_brightness(dominant, 0.5),
        }
    
    def generate_css(self):
        """生成 CSS 样式文件"""
        extractor = ColorExtractor()
        
        css = f"""/* CowAgent 自动生成主题 */
/* 基于壁纸: {os.path.basename(self.image_path)} */
/* 生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')} */

:root {{
  /* 白天模式 */
  --light-sidebar-bg: {extractor.rgb_to_hex(self.light_theme['sidebar_bg'])};
  --light-sidebar-text: {extractor.rgb_to_hex(self.light_theme['sidebar_text'])};
  --light-chat-bg: {extractor.rgb_to_hex(self.light_theme['chat_bg'])};
  --light-chat-text: {extractor.rgb_to_hex(self.light_theme['chat_text'])};
  --light-accent: {extractor.rgb_to_hex(self.light_theme['accent'])};
  --light-hover: {extractor.rgb_to_hex(self.light_theme['hover'])};
  
  /* 夜晚模式 */
  --dark-sidebar-bg: {extractor.rgb_to_hex(self.dark_theme['sidebar_bg'])};
  --dark-sidebar-text: {extractor.rgb_to_hex(self.dark_theme['sidebar_text'])};
  --dark-chat-bg: {extractor.rgb_to_hex(self.dark_theme['chat_bg'])};
  --dark-chat-text: {extractor.rgb_to_hex(self.dark_theme['chat_text'])};
  --dark-accent: {extractor.rgb_to_hex(self.dark_theme['accent'])};
  --dark-hover: {extractor.rgb_to_hex(self.dark_theme['hover'])};
}}

/* 侧边栏样式 */
.sidebar {{
  background: var(--light-sidebar-bg) !important;
  color: var(--light-sidebar-text) !important;
  transition: all 0.3s ease;
}}

.sidebar .nav-item {{
  color: var(--light-sidebar-text) !important;
}}

.sidebar .nav-item:hover {{
  background: var(--light-hover) !important;
}}

/* 聊天区域 */
.chat-container {{
  background: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), 
              url('chat-bg.jpg') !important;
  background-size: cover !important;
  background-position: center !important;
}}

/* 夜晚模式 */
@media (prefers-color-scheme: dark) {{
  .sidebar {{
    background: var(--dark-sidebar-bg) !important;
    color: var(--dark-sidebar-text) !important;
  }}
  
  .sidebar .nav-item {{
    color: var(--dark-sidebar-text) !important;
  }}
  
  .sidebar .nav-item:hover {{
    background: var(--dark-hover) !important;
  }}
  
  .chat-container {{
    background: linear-gradient(rgba(30,30,35,0.95), rgba(30,30,35,0.95)), 
                url('chat-bg.jpg') !important;
  }}
}}

/* 手动切换 */
[data-theme="dark"] .sidebar {{
  background: var(--dark-sidebar-bg) !important;
  color: var(--dark-sidebar-text) !important;
}}

[data-theme="dark"] .chat-container {{
  background: linear-gradient(rgba(30,30,35,0.95), rgba(30,30,35,0.95)), 
              url('chat-bg.jpg') !important;
}}
"""
        return css
    
    def generate_html(self):
        """生成 HTML 文件"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CowAgent - 自定义主题</title>
    <link rel="stylesheet" href="static/css/console.css">
    <link rel="stylesheet" href="static/css/custom-theme.css">
</head>
<body>
    <div class="app-container">
        <!-- 侧边栏 -->
        <aside class="sidebar">
            <div class="logo">
                <img src="static/logo.jpg" alt="Logo">
            </div>
            <nav class="nav-menu">
                <a href="#" class="nav-item active">对话</a>
                <a href="#" class="nav-item">知识库</a>
                <a href="#" class="nav-item">技能</a>
                <a href="#" class="nav-item">设置</a>
            </nav>
        </aside>
        
        <!-- 主内容区 -->
        <main class="main-content">
            <div class="chat-container">
                <!-- 聊天内容 -->
            </div>
        </main>
    </div>
    
    <script>
        // 自动检测系统主题
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
            document.documentElement.setAttribute('data-theme', 'dark');
        }}
        
        // 监听主题变化
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {{
            if (e.matches) {{
                document.documentElement.setAttribute('data-theme', 'dark');
            }} else {{
                document.documentElement.removeAttribute('data-theme');
            }}
        }});
    </script>
</body>
</html>"""
        return html
    
    def save_theme(self, output_dir):
        """保存主题文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存 CSS
        css_path = os.path.join(output_dir, 'custom-theme.css')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_css())
        
        # 保存 HTML
        html_path = os.path.join(output_dir, 'chat.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_html())
        
        # 复制壁纸
        import shutil
        bg_path = os.path.join(output_dir, 'chat-bg.jpg')
        shutil.copy2(self.image_path, bg_path)
        
        return {
            'css': css_path,
            'html': html_path,
            'background': bg_path
        }

class GeneratorThread(QThread):
    """后台生成线程"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, image_path, output_dir):
        super().__init__()
        self.image_path = image_path
        self.output_dir = output_dir
    
    def run(self):
        try:
            generator = ThemeGenerator(self.image_path)
            result = generator.save_theme(self.output_dir)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class ThemeGeneratorApp(QMainWindow):
    """主题生成器主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎸 CowAgent 主题生成器")
        self.setMinimumSize(900, 700)
        
        self.image_path = None
        self.output_dir = os.path.expanduser("~/Desktop/CowAgent-Theme")
        
        self.setup_ui()
        self.apply_style()
    
    def setup_ui(self):
        """设置界面"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("🎸 CowAgent 主题生成器")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # 副标题
        subtitle = QLabel("上传你喜欢的壁纸，自动生成适配的白天/夜晚主题")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont()
        subtitle_font.setPointSize(11)
        subtitle.setFont(subtitle_font)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # 图片预览区域
        preview_frame = QFrame()
        preview_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        preview_layout = QVBoxLayout(preview_frame)
        
        self.preview_label = QLabel("点击上传壁纸图片")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumHeight(300)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: #f0f0f0;
                border: 2px dashed #ccc;
                border-radius: 10px;
                color: #666;
                font-size: 14px;
            }
            QLabel:hover {
                background: #e8e8e8;
                border-color: #999;
            }
        """)
        self.preview_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.preview_label.mousePressEvent = lambda e: self.select_image()
        preview_layout.addWidget(self.preview_label)
        
        layout.addWidget(preview_frame)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        
        self.select_btn = QPushButton("📁 选择壁纸")
        self.select_btn.setMinimumHeight(45)
        self.select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_btn.clicked.connect(self.select_image)
        btn_layout.addWidget(self.select_btn)
        
        self.generate_btn = QPushButton("✨ 生成主题")
        self.generate_btn.setMinimumHeight(45)
        self.generate_btn.setEnabled(False)
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_btn.clicked.connect(self.generate_theme)
        btn_layout.addWidget(self.generate_btn)
        
        self.install_btn = QPushButton("🚀 安装到 CowAgent")
        self.install_btn.setMinimumHeight(45)
        self.install_btn.setEnabled(False)
        self.install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.install_btn.clicked.connect(self.install_theme)
        btn_layout.addWidget(self.install_btn)
        
        layout.addLayout(btn_layout)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # 状态信息
        self.status_label = QLabel("等待选择图片...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 颜色预览区域
        self.color_frame = QFrame()
        self.color_frame.setVisible(False)
        color_layout = QVBoxLayout(self.color_frame)
        
        color_title = QLabel("🎨 提取的颜色预览")
        color_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_layout.addWidget(color_title)
        
        self.color_preview = QLabel()
        self.color_preview.setMinimumHeight(80)
        self.color_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_layout.addWidget(self.color_preview)
        
        layout.addWidget(self.color_frame)
        
        layout.addStretch()
        
        # 底部信息
        footer = QLabel("CowAgent Theme Generator")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(footer)
    
    def apply_style(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background: #fafafa;
            }
            QPushButton {
                background: #ff6b9d;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #ff5a8c;
            }
            QPushButton:disabled {
                background: #ccc;
            }
            QPushButton#install_btn {
                background: #4CAF50;
            }
            QPushButton#install_btn:hover {
                background: #45a049;
            }
            QProgressBar {
                border: 2px solid #ff6b9d;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #ff6b9d;
            }
        """)
    
    def select_image(self):
        """选择图片"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择壁纸图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.image_path = file_path
            self.show_preview(file_path)
            self.generate_btn.setEnabled(True)
            self.status_label.setText(f"已选择: {os.path.basename(file_path)}")
    
    def show_preview(self, image_path):
        """显示图片预览"""
        pixmap = QPixmap(image_path)
        scaled = pixmap.scaled(
            self.preview_label.width() - 40,
            self.preview_label.height() - 40,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.preview_label.setPixmap(scaled)
        self.preview_label.setStyleSheet("""
            QLabel {
                background: white;
                border: 2px solid #ff6b9d;
                border-radius: 10px;
            }
        """)
    
    def generate_theme(self):
        """生成主题"""
        if not self.image_path:
            return
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # 无限进度
        self.status_label.setText("正在分析图片并生成主题...")
        self.generate_btn.setEnabled(False)
        
        # 在后台线程生成
        self.generator_thread = GeneratorThread(self.image_path, self.output_dir)
        self.generator_thread.finished.connect(self.on_generate_finished)
        self.generator_thread.error.connect(self.on_generate_error)
        self.generator_thread.start()
    
    def on_generate_finished(self, result):
        """生成完成"""
        self.progress.setVisible(False)
        self.progress.setRange(0, 100)
        
        # 显示颜色预览
        self.show_color_preview()
        
        self.status_label.setText(
            f"✅ 主题生成成功！\n"
            f"📁 保存位置: {self.output_dir}"
        )
        self.install_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        
        QMessageBox.information(
            self,
            "生成成功",
            f"主题已生成！\n\n文件位置:\n{self.output_dir}"
        )
    
    def on_generate_error(self, error_msg):
        """生成错误"""
        self.progress.setVisible(False)
        self.status_label.setText(f"❌ 生成失败: {error_msg}")
        self.generate_btn.setEnabled(True)
        
        QMessageBox.critical(self, "生成失败", error_msg)
    
    def show_color_preview(self):
        """显示颜色预览"""
        if not self.image_path:
            return
        
        generator = ThemeGenerator(self.image_path)
        extractor = ColorExtractor()
        
        # 创建颜色预览图
        preview_text = f"""
        <html>
        <body style='background: #f5f5f5; padding: 10px;'>
        <div style='display: flex; gap: 10px; justify-content: center;'>
            <div style='text-align: center;'>
                <div style='width: 60px; height: 60px; background: {extractor.rgb_to_hex(generator.light_theme["sidebar_bg"])}; border-radius: 8px; margin: 5px;'></div>
                <small>侧边栏(亮)</small>
            </div>
            <div style='text-align: center;'>
                <div style='width: 60px; height: 60px; background: {extractor.rgb_to_hex(generator.dark_theme["sidebar_bg"])}; border-radius: 8px; margin: 5px;'></div>
                <small>侧边栏(暗)</small>
            </div>
            <div style='text-align: center;'>
                <div style='width: 60px; height: 60px; background: {extractor.rgb_to_hex(generator.light_theme["accent"])}; border-radius: 8px; margin: 5px;'></div>
                <small>强调色</small>
            </div>
        </div>
        </body>
        </html>
        """
        self.color_preview.setText(preview_text)
        self.color_frame.setVisible(True)
    
    def install_theme(self):
        """安装主题到 CowAgent"""
        # 查找 CowAgent 安装目录
        cowagent_paths = [
            os.path.expanduser("~/chatgpt-on-wechat"),
            os.path.expanduser("~/CowAgent"),
            "C:/cow",
            "D:/cow",
        ]
        
        cowagent_path = None
        for path in cowagent_paths:
            if os.path.exists(os.path.join(path, "channel", "web")):
                cowagent_path = path
                break
        
        if not cowagent_path:
            # 让用户手动选择
            cowagent_path = QFileDialog.getExistingDirectory(
                self,
                "选择 CowAgent 安装目录"
            )
            if not cowagent_path:
                return
        
        try:
            import shutil
            from datetime import datetime
            
            # 备份原文件
            web_path = os.path.join(cowagent_path, "channel", "web")
            backup_dir = os.path.join(cowagent_path, "custom_backup", 
                                       datetime.now().strftime("%Y%m%d_%H%M%S"))
            os.makedirs(backup_dir, exist_ok=True)
            
            # 备份文件
            files_to_backup = [
                ("chat.html", web_path),
                ("console.css", os.path.join(web_path, "static", "css")),
            ]
            
            for filename, path in files_to_backup:
                src = os.path.join(path, filename)
                if os.path.exists(src):
                    shutil.copy2(src, backup_dir)
            
            # 安装新主题
            shutil.copy2(
                os.path.join(self.output_dir, "chat.html"),
                web_path
            )
            shutil.copy2(
                os.path.join(self.output_dir, "custom-theme.css"),
                os.path.join(web_path, "static", "css")
            )
            shutil.copy2(
                os.path.join(self.output_dir, "chat-bg.jpg"),
                os.path.join(web_path, "static")
            )
            
            QMessageBox.information(
                self,
                "安装成功",
                f"主题已安装到 CowAgent！\n\n"
                f"原文件已备份到:\n{backup_dir}\n\n"
                f"请刷新浏览器页面查看效果。"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "安装失败", str(e))

def main():
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle('Fusion')
    
    window = ThemeGeneratorApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
