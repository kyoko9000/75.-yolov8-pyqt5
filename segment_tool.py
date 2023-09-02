import sys

from PyQt5.QtCore import QRect, Qt, QThread
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog
from ultralytics import SAM

from gui2 import Ui_MainWindow


class Mylabel(QLabel):
    x0 = 0
    x1 = 0
    y0 = 0
    y1 = 0
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        # print("x0, y0: ", self.x0, self.y0)

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()
            # print("x1, y1: ", self.x1, self.y1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        rec = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter.drawRect(rec)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.cls = []
        self.rec = None
        self.link_file = None
        self.flag = False
        self.pixmap = None
        self.lb = None
        self.lb0 = []
        self.rec_list = []

        self.uic.pushButton.clicked.connect(self.load_pic)
        self.uic.pushButton_2.clicked.connect(self.make_rec)
        self.uic.pushButton_3.clicked.connect(self.delete_rec)
        self.uic.pushButton_4.clicked.connect(self.export_data)
        self.uic.pushButton_5.clicked.connect(self.add_rec)

        self.thread = {}

    def load_pic(self):
        self.link_file = QFileDialog.getOpenFileName()
        self.pixmap = QPixmap(self.link_file[0])
        self.uic.label.setPixmap(self.pixmap)

    def make_rec(self):
        self.lb = Mylabel(self)
        self.lb.setGeometry(QRect(20, 10, 650, 400))
        self.lb.setCursor(Qt.CrossCursor)
        self.lb.show()
        self.lb0.append(self.lb)
        self.flag = True

    def add_rec(self):
        self.rec_list.append(self.rec)
        self.cls.append(self.uic.lineEdit.text())
        print(self.rec_list, "\n", self.cls)
        self.make_rec()

    def delete_rec(self):
        for i in range(len(self.lb0)):
            self.lb0[i].deleteLater()
        self.lb0 = []
        self.rec_list = []
        self.make_rec()

    def mouseReleaseEvent(self, event):
        if self.flag:
            self.rectangle_data()

    def rectangle_data(self):
        # print("shape label", self.uic.label.width(), self.uic.label.height())
        # print("shape image", self.pixmap.width(), self.pixmap.height())
        # painter rectangle coordinates
        x0_ = self.lb.x0
        x1_ = self.lb.x1
        y0_ = self.lb.y0
        y1_ = self.lb.y1
        # painter rectangle coordinates change to %
        x0__ = round(x0_ / self.uic.label.width(), 2)
        x1__ = round(x1_ / self.uic.label.width(), 2)
        y0__ = round(y0_ / self.uic.label.height(), 2)
        y1__ = round(y1_ / self.uic.label.height(), 2)
        # convert % painter rectangle coordinates to real image coordinates
        x0 = round(x0__ * self.pixmap.width(), 2)
        x1 = round(x1__ * self.pixmap.width(), 2)
        y0 = round(y0__ * self.pixmap.height(), 2)
        y1 = round(y1__ * self.pixmap.height(), 2)
        self.rec = [x0, y0, x1, y1]

    def export_data(self):
        print("export", self.rec_list)
        class_ids = self.cls
        link = self.link_file[0]
        boxes = self.rec_list  # Boxes object for bbox outputs

        self.thread[1] = run_thread(index=1, class_ids=class_ids, link=link, boxes=boxes)
        self.thread[1].start()


class run_thread(QThread):
    def __init__(self, index, class_ids, link, boxes):
        super().__init__()
        self.index = index
        self.class_ids = class_ids
        self.link = link
        self.boxes = boxes
        print("run thread: ", self.index, self.class_ids)

    def run(self):
        sam_model = SAM('sam_b.pt')
        if len(self.boxes):
            sam_results = sam_model(self.link, bboxes=self.boxes, save=True)
            segments = sam_results[0].masks.xyn  # noqa
            name = self.link.split("/")[-1][:-4]

            with open(f'labels/{name}.txt', 'w') as f:
                for i in range(len(segments)):
                    s = segments[i]
                    if len(s) == 0:
                        continue
                    segment = map(str, segments[i].reshape(-1).tolist())
                    f.write(f'{self.class_ids[i]} ' + ' '.join(segment) + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
