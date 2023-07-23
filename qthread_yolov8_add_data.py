import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from ultralytics import YOLO

from gui1 import Ui_MainWindow


class mylabel(QLabel):
    y0 = 0
    x0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        print("start cap", self.x0, self.y0)

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
            print("move", self.x1, self.y1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        rec = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter.drawRect(rec)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.qt_img = None
        self.take = False
        self.lb = None
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.Button_start.clicked.connect(self.start_capture_video)
        self.uic.Button_take.clicked.connect(self.take_pics)

        self.thread = {}

    def mouseReleaseEvent(self, event):
        if self.take:
            data = [self.lb.y0, self.lb.y1, self.lb.x0, self.lb.x1]
            self.uic.label_2.setPixmap(self.qt_img)
            self.thread[1].take_pic(data)

    def take_pics(self):
        data = [165, 202, 90, 127]
        self.thread[1].take_pic(data)
        self.lb = mylabel(self)
        self.lb.setGeometry(QRect(20, 0, 331, 251))
        self.lb.setCursor(Qt.CrossCursor)
        self.lb.show()

    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)
        self.thread[1].signal_1.connect(self.show_pic)

    def show_pic(self, pic, data):
        self.take = True
        print(data)
        self.qt_img = self.convert_cv_qt(pic)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label_1.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        label_h = self.uic.label_1.height()
        lebel_w = self.uic.label_1.width()
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(lebel_w, label_h, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class live_stream(QThread):
    signal = pyqtSignal(object)
    signal_1 = pyqtSignal(object, object)

    def __init__(self, index):
        self.data = None
        self.pic = False
        self.index = index
        print("start threading", self.index)
        super(live_stream, self).__init__()

    def run(self):
        model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
        results = model('video1.mp4', show=True, stream=True)  # List of Results objects

        for result, frame in results:
            # boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
            # for box in boxes:  # there could be more than one detection
            #     print("class", box.cls)
            #     print("xyxy", box.xyxy)
            #     print("conf", box.conf)
            self.signal.emit(frame)
            if self.pic:
                self.signal_1.emit(frame, self.data)
                self.pic = False

    def take_pic(self, data):
        self.pic = True
        self.data = data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
