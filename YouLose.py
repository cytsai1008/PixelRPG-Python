import argparse
import sys

from PySide2 import QtWidgets
from PySide2.QtGui import QFontDatabase

from You_Lose import Ui_Form

parser = argparse.ArgumentParser()
parser.add_argument("--lv", type=int, default=0)

args = parser.parse_args()

level = args.lv


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        QFontDatabase.addApplicationFont("Launcher Asset/unifont-14.0.01.ttf")
        if level >= 5:
            self.ui.label_2.setText(
                f"Wow! You are better than 99% of the players!\n"
                f"You died at Lv.{level}!"
            )
        else:
            self.ui.label_2.setText(f"You died at Lv.{level}!\n" f"Keep going!")


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
