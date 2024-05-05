import sys
import cv2
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

        self.thread = {}
        self.count = 2

    def start_capture_video(self):
        for i in range(self.count):
            self.thread[i] = live_stream(index=i)
            self.thread[i].start()
            self.thread[i].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img, index):
        """Updates the image_label with a new opencv image"""
        if index == 0:
            qt_img = convert_cv_qt(cv_img)
            self.uic.label_1.setPixmap(qt_img)
        elif index == 1:
            qt_img = convert_cv_qt(cv_img)
            self.uic.label_2.setPixmap(qt_img)


def convert_cv_qt(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(700, 500, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


class live_stream(QThread):
    signal = pyqtSignal(object, object)

    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(live_stream, self).__init__()

    def run(self):
        model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
        results = model(f'video{self.index}.mp4', stream=True)  # List of Results objects

        for result in results:
            frame = result.plot()
            # boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
            # for box in boxes:  # there could be more than one detection
            #     print("class", box.cls)
            #     print("xyxy", box.xyxy)
            #     print("conf", box.conf)
            self.signal.emit(frame, self.index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
