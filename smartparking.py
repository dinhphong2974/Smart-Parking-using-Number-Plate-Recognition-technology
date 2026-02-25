from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys
import cv2
import pytesseract
import easyocr
import serial
import time
#import os   

import mysql.connector

db = mysql.connector.connect(
    host="localhost",        
    user="root",    
    password="PH0NG29t704:)",
    database="ds_bienso" 
)
cursor = db.cursor()

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
harcascade = r"C:/Python/Training/haarcascade_russian_plate_number.xml"


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        MainWindow.setStyleSheet("border-image: url(:/picture/bgr.png) no-repeat center center fixed;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("") 

        self.view_cam_in = QtWidgets.QLabel(self.centralwidget)
        self.view_cam_in.setGeometry(QtCore.QRect(280, 210, 641, 351))
        self.view_cam_in.setText("")
        self.view_cam_in.setObjectName("view_cam_in")
        self.view_cam_in.setAlignment(QtCore.Qt.AlignCenter)

        self.view_cam_out = QtWidgets.QLabel(self.centralwidget)
        self.view_cam_out.setGeometry(QtCore.QRect(1000, 210, 640, 360))
        self.view_cam_out.setText("")
        self.view_cam_out.setObjectName("view_cam_out")
        self.view_cam_out.setAlignment(QtCore.Qt.AlignCenter)

        self.view_bien_in = QtWidgets.QLabel(self.centralwidget)
        self.view_bien_in.setGeometry(QtCore.QRect(420, 610, 431, 81))
        self.view_bien_in.setStyleSheet("border-image: url(:/picture/Artboard 1button new.png);")
        self.view_bien_in.setText("")
        self.view_bien_in.setObjectName("view_bien_in")

        self.view_bien_out = QtWidgets.QLabel(self.centralwidget)
        self.view_bien_out.setGeometry(QtCore.QRect(1150, 610, 431, 81))
        self.view_bien_out.setStyleSheet("border-image: url(:/picture/Artboard 1button new.png);")
        self.view_bien_out.setText("")
        self.view_bien_out.setObjectName("view_bien_out")

        self.text_bien = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_bien.setGeometry(QtCore.QRect(420, 745, 431, 81))
        self.text_bien.setStyleSheet("border-image: url(:/picture/Artboard 1button new.png);")
        self.text_bien.setObjectName("text_bien")
        self.text_bien.setAlignment(QtCore.Qt.AlignCenter)

        self.img_name = QtWidgets.QLabel(self.centralwidget)
        self.img_name.setGeometry(QtCore.QRect(0, 0, 500, 50))
        self.img_name.setStyleSheet("border-image: url(:/anpham/Artboard 1bang_ten.png);")
        self.img_name.setText("")
        self.img_name.setObjectName("img_name")

        self.nut_save = QtWidgets.QPushButton(self.centralwidget)
        self.nut_save.setGeometry(QtCore.QRect(1100, 740, 101, 101))
        self.nut_save.setStyleSheet("border-image: url(:/picture/Artboard 1button save.png);")
        self.nut_save.setText("")
        self.nut_save.setObjectName("nut_save")

        self.nut_check = QtWidgets.QPushButton(self.centralwidget)
        self.nut_check.setGeometry(QtCore.QRect(1280, 740, 101, 101))
        self.nut_check.setStyleSheet("border-image: url(:/picture/Artboard 1button check.png);")
        self.nut_check.setText("")
        self.nut_check.setObjectName("nut_check")

        self.nut_thoat = QtWidgets.QPushButton(self.centralwidget)
        self.nut_thoat.setGeometry(QtCore.QRect(1722, 920, 161, 101))
        self.nut_thoat.setStyleSheet("border-image: url(:/picture/Artboard 1button exit.png);")
        self.nut_thoat.setText("")
        self.nut_thoat.setObjectName("nut_thoat")

        self.trang_thai = QtWidgets.QTextBrowser(self.centralwidget)
        self.trang_thai.setGeometry(QtCore.QRect(1450, 740, 101, 101))
        self.trang_thai.setStyleSheet("""
            border-image: url(:/picture/Artboard 1button slot.png) no-repeat;
            background-color: transparent;  
        """)        
        self.trang_thai.setObjectName("trang_thai")

        self.img_viewbien_in = QtWidgets.QLabel(self.centralwidget)
        self.img_viewbien_in.setGeometry(QtCore.QRect(340, 610, 81, 81))
        self.img_viewbien_in.setStyleSheet("border-image: url(:/picture/Artboard 3button new.png);")
        self.img_viewbien_in.setText("")
        self.img_viewbien_in.setObjectName("img_viewbien_in")

        self.img_textbien = QtWidgets.QLabel(self.centralwidget)
        self.img_textbien.setGeometry(QtCore.QRect(340, 745, 81, 81))
        self.img_textbien.setStyleSheet("border-image: url(:/picture/Artboard 3button new 2.png);")
        self.img_textbien.setText("")
        self.img_textbien.setObjectName("img_textbien")

        self.img_viewbien_out = QtWidgets.QLabel(self.centralwidget)
        self.img_viewbien_out.setGeometry(QtCore.QRect(1070, 610, 81, 81))
        self.img_viewbien_out.setStyleSheet("border-image: url(:/picture/Artboard 3button new.png);")
        self.img_viewbien_out.setText("")
        self.img_viewbien_out.setObjectName("img_viewbien_out")

        self.view_cam_in.raise_()
        self.view_cam_out.raise_()
        self.view_bien_in.raise_()
        self.view_bien_out.raise_()
        self.text_bien.raise_()
        self.nut_thoat.raise_()
        self.nut_save.raise_()
        self.nut_check.raise_()
        self.trang_thai.raise_()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.nut_thoat.clicked.connect(self.exit_app)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.trang_thai.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

    def exit_app(self):
        QApplication.quit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.img_bienso_in = None

        try:
            # Kết nối với ESP32 qua Serial (thay 'COMx' bằng cổng Serial của ESP32)
            self.serial_connection = serial.Serial(port='COM9', baudrate=115200, timeout=1)  # Đảm bảo cổng và tốc độ baudrate đúng
        except serial.SerialException as e:
            print(f"Lỗi kết nối Serial: {e}")
            self.serial_connection = None

        # Tạo một QTimer để gọi update() mỗi 100 ms
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)  # Gọi hàm update() mỗi lần timeout
        self.timer.start(100)  # 100ms (0.1s)

        # Mở camera
        self.cap0 = cv2.VideoCapture(1)
        self.cap1 = cv2.VideoCapture(0)

        self.timer_video = QTimer(self)
        self.timer.timeout.connect(self.view_video_in)
        self.timer.timeout.connect(self.view_video_out)

        self.timer.start(30)  # Cập nhật mỗi 30ms (~33 FPS)

        # Cascade cho biển số xe
        self.plate_cascade = cv2.CascadeClassifier(harcascade)     
        self.min_area = 500  # Diện tích tối thiểu để nhận diện biển số

        self.count = 757
        self.count_check = 0

        self.ui.nut_save.clicked.connect(self.save_and_show)
        self.ui.nut_check.clicked.connect(self.check_bienso)

    def read_serial_data(self):
        if self.serial_connection.in_waiting > 0:
            data = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
            if data == "Welcome In":
                self.save_and_show()  #Gọi luôn hàm save_and_show()
            elif data == "checkout_started":
                self.ui.text_bien.setText("Checkout started")
                self.check_bienso()

    def view_video_in(self):
        ret, frame = self.cap0.read()
        if not ret or frame is None:
            print("⚠ Không nhận được frame từ cap0")
            return

        # Chuyển từ BGR (OpenCV) sang RGB (PyQt)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Chuyển thành QImage
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Hiển thị video trên view_cam_in
        self.ui.view_cam_in.setPixmap(QPixmap.fromImage(qimg))

        # Biến đổi sang ảnh xám để nhận diện biển số
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Phát hiện biển số xe
        plates = self.plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > self.min_area:
                # Vẽ hình chữ nhật quanh biển số
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

                # Cắt vùng biển số
                self.img_roi_in = frame[y: y + h, x: x + w]
                self.img_roi_rgb_in = cv2.cvtColor(self.img_roi_in, cv2.COLOR_BGR2RGB)  # Lưu thành thuộc tính

                # Chuyển ảnh ROI thành QImage để hiển thị trên view_bien_in
                h, w, ch = self.img_roi_rgb_in.shape
                bytes_per_line = ch * w
                qimg_roi = QImage(self.img_roi_rgb_in.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.ui.view_bien_in.setPixmap(QPixmap.fromImage(qimg_roi))

    def view_video_out(self):
        ret, frame = self.cap1.read()
        if not ret or frame is None:
            print("⚠ Không nhận được frame từ cap1")
            return

        # Chuyển từ BGR (OpenCV) sang RGB (PyQt)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Chuyển thành QImage
        h, w, ch = img.shape
        bytes_per_line = ch * w
        qimg = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Hiển thị video trên view_cam_in
        self.ui.view_cam_out.setPixmap(QPixmap.fromImage(qimg))

        # Biến đổi sang ảnh xám để nhận diện biển số
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Phát hiện biển số xe
        plates = self.plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > self.min_area:
                # Vẽ hình chữ nhật quanh biển số
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

                # Cắt vùng biển số
                self.img_roi_out = frame[y: y + h, x: x + w]
                self.img_roi_rgb_out = cv2.cvtColor(self.img_roi_out, cv2.COLOR_BGR2RGB)  

                # Chuyển ảnh ROI thành QImage để hiển thị trên view_bien_in
                h, w, ch = self.img_roi_rgb_out.shape
                bytes_per_line = ch * w
                qimg_roi = QImage(self.img_roi_rgb_out.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.ui.view_bien_out.setPixmap(QPixmap.fromImage(qimg_roi))

    def save_and_show(self):
        if not hasattr(self, 'img_roi_in'):
            print("Không tìm thấy biển số, không thể lưu ảnh!")
            return

        file_name = f"C:/Python/plates/scanned_img_" + str(self.count) + ".jpg"
        cv2.imwrite(file_name, self.img_roi_in)

        lastimg = cv2.imread(file_name)
        gray = cv2.cvtColor(lastimg, cv2.COLOR_BGR2GRAY)
        reader = easyocr.Reader(['en'])
        self.bienso = reader.readtext(gray)

        if self.bienso:
            self.text_bienso = self.bienso[0][-2]
            print(f"Extracted Text: {self.text_bienso}")
            self.send_command(str(self.text_bienso))
        else:
            print("OCR không thể nhận diện biển số.")
            self.ui.text_bien.setText("Không nhận diện được biển số!")
            return

        # Đảm bảo text biển số không rỗng
        if not self.text_bienso:
            print("Không có biển số để lưu.")
            return

        try:
            query = "INSERT INTO `ds_bienso`.`ds_bienso` (`stt`, `ds_bienso`) VALUES (%s, %s);"
            values = (self.count, self.text_bienso)
            cursor.execute(query, values)
            db.commit()
        except mysql.connector.Error as err:
            print(f" Lỗi MySQL: {err}")
            if "Duplicate entry" in str(err):
                self.count += 1
            return

        self.ui.text_bien.setText(f"Biển số: {self.text_bienso}")
        self.ui.text_bien.setStyleSheet("color: green; font-size: 24px; font-weight: bold;")
        self.count += 1

    def check_bienso(self):
        time.sleep(1)
        if not hasattr(self, 'img_roi_out'):
            print("Không tìm thấy biển số để kiểm tra!")
            return  # Thoát khỏi hàm nếu không có biển số ở camera 'out'
        
        # Đặt đường dẫn lưu tệp
        file_name = f"C:/Python/plates/checked_img_" + str(self.count_check) + ".jpg"
        cv2.imwrite(file_name, self.img_roi_out)  
        print(f"Ảnh được lưu tại: {file_name}")

        lastimg = cv2.imread(file_name)

        gray = cv2.cvtColor(lastimg, cv2.COLOR_BGR2GRAY)      
        reader = easyocr.Reader(['en']) 
        self.bienso_sau = reader.readtext(gray)
        if self.bienso_sau:  # Nếu danh sách không rỗng
            self.text_bienso_sau = self.bienso_sau[0][-2]
            print(f"Checked: {self.text_bienso_sau}")
            self.send_command(str(self.text_bienso_sau))

        else:
            print("OCR không thể nhận diện biển số.")
            self.ui.text_bien.setText("Không nhận diện được biển số!")
            return

        # bienso checked
        input_bienso = self.text_bienso_sau

        # Kiểm tra bienso trong cột `ds_bienso`
        query_check = "SELECT COUNT(*) FROM ds_bienso WHERE ds_bienso = %s"
        values = (input_bienso,)

        cursor.execute(query_check, values)
        self.result = cursor.fetchone()

        if self.result[0] > 0:
            self.send_command('1')
        else:
            self.send_command('0')

        self.update_trang_thai()
        self.count_check = self.count_check + 1

    def update_trang_thai(self):
        self.so_cho_trong = 5 - self.count + self.count_check + 757
    # Cập nhật số ô trống lên giao diện
        if self.so_cho_trong > 0:
            self.ui.trang_thai.setStyleSheet("color: green; font-size: 32px; font-weight: bold;")
            self.ui.trang_thai.setText(str(self.so_cho_trong))
        else:
            self.ui.trang_thai.setStyleSheet("color: red; font-size: 32px; font-weight: bold;")
            self.ui.trang_thai.setText(f"Full")

    def send_command(self, command):
        """Gửi lệnh tới ESP32 qua Serial."""
        if self.serial_connection:
            self.serial_connection.write((command + '\n').encode())  # Gửi lệnh qua Serial
            print(f"Đã gửi lệnh: {command}")

    def update(self):
        self.read_serial_data()  # Gọi hàm để đọc và xử lý dữ liệu từ ESP32

    def closeEvent(self, event):
        self.cap0.release()
        self.cap1.release()  

        if self.serial_connection:
            self.serial_connection.close()
        event.accept()
        
import artboard_qrc

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
