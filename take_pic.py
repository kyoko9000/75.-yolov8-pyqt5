import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from ultralytics import YOLO

from gui1 import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.Button_start.clicked.connect(self.start_capture_video)
        self.uic.Button_stop.clicked.connect(self.take_pics)

        self.thread = {}

    def take_pics(self):
        self.thread[1].take_pic()

    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)
        self.thread[1].signal_1.connect(self.show_pic)

    def show_pic(self, pic):
        # cv2.imshow('frame', pic)
        qt_img = self.convert_cv_qt(pic)
        self.uic.label_2.setPixmap(qt_img)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label_1.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        label_W = self.uic.label_1.width()
        label_H = self.uic.label_1.height()
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(label_W, label_H, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class live_stream(QThread):
    signal = pyqtSignal(object)
    signal_1 = pyqtSignal(object)

    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(live_stream, self).__init__()
        self.pic = False

    def run(self):
        cap = cv2.VideoCapture("video1.mp4")

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            self.signal.emit(frame)
            if self.pic:
                self.signal_1.emit(frame)
                self.pic = False
                print(self.pic)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    def take_pic(self):
        self.pic = True



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
