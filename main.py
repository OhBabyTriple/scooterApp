import os
import sys

# 添加项目根目录到Python路径，确保可以正确导入src包
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.views.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.run() 