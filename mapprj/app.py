import sys
import logging
from threading import Thread
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from server import storage, api

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')

if __name__ == '__main__':
    storage.reset_positions_file()
    logging.info("🔄 Đã reset positions.json")
    t = Thread(target=api.run_server, daemon=True)
    t.start()
    logging.info("🌐 Flask server chạy tại http://0.0.0.0:5000")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
