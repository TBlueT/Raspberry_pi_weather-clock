import datetime as dt
from img.opencv import number_img
from PyQt5 import QtTest, QtCore
class timerun(QtCore.QThread):
    def __init__(self, MainWindow, wt , parent=None):
        super(timerun, self).__init__(parent)

        self.MainWindow = MainWindow
        self.wt = wt
        self.nimg = number_img()
        self.Day = []
        self.hour = []
        self.Day_old = []
        self.hour_old = [0,0,0]
        self.hour_str = [[]for _ in range(0, 3)]
        self.img_count = 1

    def run(self):
        while True:
            time_now = dt.datetime.now()

            self.Day = [time_now.year] + [time_now.month] + [time_now.day]
            self.hour = [time_now.hour] + [time_now.minute] + [time_now.second]

            if self.Day[2] != self.Day_old:
                self.MainWindow.time_Day.setText(
                    str(self.Day[0]) + 'Year ' + str(self.Day[1]) + 'Month ' + str(self.Day[2]) + 'Day')

            self.Hour_process()
            self.Minute_process()
            self.Second_process()
            
            self.Day_old = self.Day[2]
            self.hour_old = self.hour

            QtTest.QTest.qWait(0.1*1000)

    def Hour_process(self):
        if self.hour[0] != self.hour_old[0]:
            self.MainWindow.Hour.setPixmap(self.nimg.printing(self.hour[0]))
            for i in range(1, 8):
                hour = self.hour[0] + i
                getattr(self.MainWindow, 'time_T_' + str(i)).setText(
                    ('0'+str(hour-24) if (hour > 23) else (str(hour) if (hour > 9) else '0'+str(hour))) + ":00")

    def Minute_process(self):
        if self.hour[1] != self.hour_old[1]:
            self.MainWindow.Minute.setPixmap(self.nimg.printing(self.hour[1]))
            if (self.wt.API_reconnect == False) and int(self.hour[1]%100/10) != int(self.hour_old[1]%100/10):
                self.wt.start()

            elif (self.wt.API_reconnect == True) and int(self.hour[1]%10/1) != int(self.hour_old[1]%10/1):
                self.wt.API_reconnect = False
                self.wt.start()

    def Second_process(self):
        if self.hour[2] != self.hour_old[2]:
            self.MainWindow.Second.setPixmap(self.nimg.printing(self.hour[2]))
