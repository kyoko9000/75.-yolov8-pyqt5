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
        self.uic.Button_take.clicked.connect(self.take_pics)

        self.thread = {}

    def take_pics(self):
        self.thread[1].take_pic()

    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)
        self.thread[1].signal_1.connect(self.show_pic)

    def show_pic(self, pic):
        qt_img = self.convert_cv_qt(pic)
        self.uic.label_2.setPixmap(qt_img)

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
    signal_1 = pyqtSignal(object)

    def __init__(self, index):
        self.pic = False
        self.index = index
        print("start threading", self.index)
        super(live_stream, self).__init__()

    def run(self):
        model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
        results = model('video.mp4', show=True, stream=True)  # List of Results objects

        # def show_frame():
        #     cv2.imshow("show", frame)
        #     cv2.waitKey(1)

        for result, frame in results:
            # show_frame()
            # boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
            # for box in boxes:  # there could be more than one detection
            #     print("class", box.cls)
            #     print("xyxy", box.xyxy)
            #     print("conf", box.conf)
            self.signal.emit(frame)
            if self.pic:
                self.signal_1.emit(frame)
                self.pic = False

    def take_pic(self):
        self.pic = True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
