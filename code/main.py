import sys

from PyQt5.QtWidgets import  *
from PyQt5 import uic
from PyQt5.QtCore import *
from WeatherData import *
from TimeProcess import *


GUI_class = uic.loadUiType('ui.ui')[0]

class mainWindow(QMainWindow, GUI_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        #self.showFullScreen()
        self.stackedWidget.setCurrentIndex(0)
        print(self.height(),self.width())

        self.wt = Weather(self)
        self.tP = timerun(self)

        self.tP.Set_Text.connect(self.Set_Text)
        self.wt.Set_Text.connect(self.Set_Text)
        self.wt.Set_StyleSheet.connect(self.Set_StyleSheet)

    def Set_Pixmap(self, object, data):
        getattr(self, object).setPixmap(data)

    @pyqtSlot(str, str)
    def Set_Text(self, object, data):
        getattr(self, object).setText(data)

    @pyqtSlot(str, str)
    def Set_StyleSheet(self, object, data):
        getattr(self, object).setStyleSheet(data)


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.tP.processing = False
            self.close()

    def runThread(self):
        self.tP.start()

def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)

    sys._excepthook(exctype, value, traceback)

if __name__ == "__main__":
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    app.aboutToQuit.connect(mainWindow)
    MainWindow = mainWindow()
    MainWindow.show()
    MainWindow.runThread()

    app.exec()