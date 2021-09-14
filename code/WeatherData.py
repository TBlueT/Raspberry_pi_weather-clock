from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from collections import OrderedDict
import requests
import json
import datetime as dt

class Weather(QtCore.QThread):
    def __init__(self, MainWindow, parent=None):
        super(Weather, self).__init__(parent)

        self.MainWindow = MainWindow

        iconimg_name = ['01', '02', '03', '04', '09', '10', '11', '13', '50']
        for i in iconimg_name:
            setattr(self, i +'d', QPixmap('img/Weather/' + i + 'd.png'))
        for i in iconimg_name:
            setattr(self, i + 'n', QPixmap('img/Weather/' + i + 'n.png'))
        self.API_address = 'https://api.openweathermap.org/data/2.5/onecall?lat=35.54&lon=129.43&units=metric&exclude=daily&appid=0f1315f6157ab87ca9cad438062c6a0b&lang=kr'
        self.data = OrderedDict()
        self.k2c = lambda k: k - 273.15
        self.API_reconnect = False

        self.time_T = [0, 0, 0, 0, 0, 0, 0]
        self.time_Temperature()

    def run(self):
        try:
            # self.API_get = requests.get(
            #     'https://api.openweathermap.org/data/2.5/onecall?lat=36.32&lon=127.33&exclude=daily&appid=0f1315f6157ab87ca9cad438062c6a0b&lang=kr')
            API_get = requests.get(self.API_address)
            self.data = json.loads(API_get.text)
            print(self.data)
            if self.data["timezone"] == "Asia/Seoul":
                self.MainWindow.Li_text.setText("위치: 울산")
                self.MainWindow.Description_Text.setText("날시: "+self.data["current"]["weather"][0]["description"])
                self.MainWindow.weather_img.setPixmap(self.img_number(self.data["current"]["weather"][0]['icon']))
                self.MainWindow.Temperature_Text.setText("온도: "+str(int(self.data["hourly"][0]["temp"]))+"'C")
                self.MainWindow.Other_Text.setText('습도:'+str(self.data["current"]["humidity"])+'%'+'\n'+'풍향:'+str(self.data["current"]["wind_deg"])+"'"+'\n'+'풍속:'+str(self.data["current"]["wind_speed"])+'m/s')

                for i in range(1, 8):
                    getattr(self.MainWindow, 'time_T_n_' + str(i)).setText(
                        str(int(self.data["hourly"][i]["temp"])) + "'C")

            else:
                self.API_reconnect = True
                self.MainWindow.Li_text.setText("API연결 오류")
                self.MainWindow.Description_Text.setText("재접속 시도중...")
                self.MainWindow.Temperature_Text.setText("약 1분소요될예정")
                self.MainWindow.Other_Text.setText('')
                print(self.data)

        except:
            self.MainWindow.Li_text.setText("wifi 없음")
            self.MainWindow.Description_Text.setText("wifi연결을 확인해 주세요")
            self.MainWindow.Temperature_Text.setText('')
            self.MainWindow.Other_Text.setText('')
            self.MainWindow.weather_img.setPixmap(QPixmap('img/Internet.png'))


    def img_number(self, number):
        return getattr(self, number, lambda: 'default')

    def time_Temperature(self):
        for i in range(0,len(self.time_T)):
            if self.time_T[i] <= 0:
                getattr(self.MainWindow, 'time_T_n_' + str(i+1)).setStyleSheet("color: #0000FF")

    def time_Temperature_Time(self):
        hour = dt.datetime.now().hour
        for i in range(1, 8):
            getattr(self.MainWindow, 'time_T_' + str(i)).setText(str((hour+i)-24 if hour+i > 23 else hour+i)+":00")
            getattr(self.MainWindow, 'time_T_n_' + str(i)).setText(str(int(round(self.k2c(self.data["hourly"][i]["temp"]),0)))+"'C")
