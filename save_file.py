import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from gui2 import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.pushButton.clicked.connect(self.save)

    def save(self):
        filename = "filename"
        path = QFileDialog.getSaveFileName(None, "save file", filename, ".txt")
        if len(path) == 0:
            return
        path_str = ''.join(path)

        text_file = open(path_str, "w")
        text_file.write("self.__console.toPlainText()")
        text_file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())