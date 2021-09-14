import sys

from PyQt5.QtWidgets import  *
from PyQt5 import uic
from WeatherData import *
from TimeProcess import *

GUI_class = uic.loadUiType('ui.ui')[0]

class mainWindow(QMainWindow, GUI_class):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        #self.showFullScreen()
        self.stackedWidget.setCurrentIndex(0)
        self.wifi_scan = []
        self.wifi_button_pus = [""]
        print(self.height(),self.width())

        self.wt = Weather(self)
        self.tP = timerun(self, self.wt)
        self.tP.start()


    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key_Escape:
    #         self.close()



def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = mainWindow()
    MainWindow.show()

    app.exec()