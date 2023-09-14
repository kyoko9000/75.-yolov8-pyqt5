import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui2 import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.pushButton.clicked.connect(self.open)
        self.uic.pushButton_2.clicked.connect(self.save)

    def open(self):
        # default_path = "D:/2. Python projects"
        default_path = ""
        self.path, _ = QFileDialog.getOpenFileName(None, "open file", default_path, "*.txt")
        print(self.path)

    def save(self):
        try:
            filename = self.path  # filename or default path to file
            path, _ = QFileDialog.getSaveFileName(None, "save file", filename, "*.txt")
            print(path)
            if len(path) == 0:
                return

            text_file = open(path, "w")
            text_file.write("test message")
            text_file.close()
        except:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
