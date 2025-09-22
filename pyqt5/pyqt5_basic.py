import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import uic

get_path = os.path.dirname(os.path.realpath(__file__))
form_class = uic.loadUiType(get_path+"\\파일이름.ui")[0]


class mainWidget(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_window = mainWidget()
    app_window.show()
    app.exec_()
