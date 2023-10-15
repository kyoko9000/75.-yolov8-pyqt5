import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.Button_start.setText("load file")
        self.uic.Button_stop.setText("save file")
        self.uic.Button_start.clicked.connect(self.open)
        self.uic.Button_stop.clicked.connect(self.save)

    def open(self):
        try:
            # default_path = "D:/2. Python projects"
            default_path = ""
            self.path, _ = QFileDialog.getOpenFileName(None, "open file", default_path, "*.txt")
            text_file = open(self.path, "r")
            self.uic.label.setText(text_file.read())
            font = QtGui.QFont()
            font.setPointSize(30)
            self.uic.label.setFont(font)
            print(self.path)
        except:
            pass

    def save(self):
        try:
            filename = self.path  # filename or default path to file
            path, _ = QFileDialog.getSaveFileName(None, "save file", filename, "*.txt")
            print(path)
            if len(path) == 0:
                return

            text_file = open(path, "w")
            text_file.write("write your text here 3")
            text_file.close()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
