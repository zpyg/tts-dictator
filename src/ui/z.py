from PyQt5 import QtCore, QtGui, QtWidgets
from x import Ui_MainWindow
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        self.say()
        super().__init__()

    def say(self):
        print("hello, world")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    Ui_MainWindow().setupUi(win)
    win.show()
    sys.exit(app.exec_())
