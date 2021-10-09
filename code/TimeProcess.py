import datetime as dt
from img.opencv import number_img
from PyQt5 import QtTest, QtCore, QtWidgets
class timerun(QtCore.QThread):
    Set_Text = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(timerun, self).__init__(parent)
        self.processing = True

        self.MainWindow = parent
        self.wt = self.MainWindow.wt
        self.nimg = number_img()
        self.Day = []
        self.hour = []
        self.Day_old = []
        self.hour_old = [0,0,0]
        self.hour_str = [[]for _ in range(0, 3)]
        self.img_count = 1

    def run(self):
        while self.processing:
            time_now = dt.datetime.now()

            self.Day = [time_now.year] + [time_now.month] + [time_now.day]
            self.hour = [time_now.hour] + [time_now.minute] + [time_now.second]

            if self.Day[2] != self.Day_old:
                self.Set_Text.emit("time_Day",
                                   F"{self.Day[0]}Year {self.Day[1]}Month {self.Day[2]}Day")

            self.Hour_process()
            self.Minute_process()
            self.Second_process()
            
            self.Day_old = self.Day[2]
            self.hour_old = self.hour

            QtTest.QTest.qWait(0.1*1000)

    def Hour_process(self):
        if self.hour[0] != self.hour_old[0]:
            self.MainWindow.Set_Pixmap("Hour", self.nimg.printing(self.hour[0]))
            for i in range(1, 8):
                hour = self.hour[0] + i
                self.Set_Text.emit(F"time_T_{i}", F"{'0' + str(hour - 24) if (hour > 23) else (str(hour) if (hour > 9) else '0' + str(hour))}:00")
    def Minute_process(self):
        if self.hour[1] != self.hour_old[1]:
            self.MainWindow.Set_Pixmap("Minute", self.nimg.printing(self.hour[1]))
            if (self.wt.API_reconnect == False) and int(self.hour[1]%100/10) != int(self.hour_old[1]%100/10):
                self.wt.start()

            elif (self.wt.API_reconnect == True) and int(self.hour[1]%10/1) != int(self.hour_old[1]%10/1):
                self.wt.API_reconnect = False
                self.wt.start()

    def Second_process(self):
        if self.hour[2] != self.hour_old[2]:
            self.MainWindow.Set_Pixmap("Second", self.nimg.printing(self.hour[2]))
            #self.MainWindow.Second.reoaint()
