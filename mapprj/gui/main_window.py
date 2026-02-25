import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import logging
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UAV Tracker - PyQt")
        self.resize(900, 700)
        self.browser = QWebEngineView()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        map_path = os.path.join(base_dir, "..", "map.html")
        if not os.path.exists(map_path):
            logging.error(f"Không tìm thấy map.html tại: {map_path}")
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath(map_path)))
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.browser)
        self.setCentralWidget(container)
        logging.info("Đã tải map.html lên PyQt WebView.")
