from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui
from collections import OrderedDict
import requests
import json
import datetime as dt

class Weather(QtCore.QThread):
    Set_Text = QtCore.pyqtSignal(str, str)
    Set_Pixmap = QtCore.pyqtSignal(str, QtGui.QPixmap)
    Set_StyleSheet = QtCore.pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(Weather, self).__init__(parent)

        self.MainWindow = parent

        iconimg_name = ['01', '02', '03', '04', '09', '10', '11', '13', '50']
        for i in iconimg_name:
            setattr(self, i +'d', QPixmap('img/Weather/' + i + 'd.png'))
        for i in iconimg_name:
            setattr(self, i + 'n', QPixmap('img/Weather/' + i + 'n.png'))
        self.API_address = 'https://api.openweathermap.org/data/2.5/onecall?lat=36.32&lon=127.34&units=metric&exclude=daily&appid=0f1315f6157ab87ca9cad438062c6a0b&lang=kr'
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
                self.Set_Text.emit("Li_text", "위치: 대전")
                self.Set_Text.emit("Description_Text", "날시: "+str(self.data['current']['weather'][0]['description']))
                self.Set_Pixmap.emit("weather_img", self.img_number(self.data['current']['weather'][0]['icon']))
                self.Set_Text.emit("Temperature_Text", "온도: "+str(int(self.data['hourly'][0]['temp']))+"'C")
                self.Set_Text.emit("Other_Text", '습도:'+str(self.data["current"]["humidity"])+'%'+'\n'+'풍향:'+str(self.data["current"]["wind_deg"])+"'"+'\n'+'풍속:'+str(self.data["current"]["wind_speed"])+'m/s')

                for i in range(1, 8):
                    self.Set_Text.emit(F"time_T_n_{i}", str(int(self.data["hourly"][i]["temp"])) + "'C")
                    self.Set_Pixmap.emit(F"time_T_n_i_{i}", self.img_number(self.data["hourly"][i]["weather"][0]["icon"]))

            else:
                self.API_reconnect = True
                self.Set_Text.emit("Li_text", "API연결 오류")
                self.Set_Text.emit("Description_Text", "재접속 시도중...")
                self.Set_Text.emit("Temperature_Text", "약 1분소요될예정")
                self.Set_Text.emit("Other_Text", '')
                print(self.data)

        except:
            self.Set_Text.emit("Li_text", "wifi 없음")
            self.Set_Text.emit("Description_Text", "연결을 확인해 주세요")
            self.Set_Text.emit("Temperature_Text", '')
            self.Set_Text.emit("Other_Text", '')
            self.Set_Pixmap.emit("weather_img", QPixmap('img/Internet.png'))


    def img_number(self, number):
        return getattr(self, number, lambda: 'default')

    def time_Temperature(self):
        for i in range(0,len(self.time_T)):
            if self.time_T[i] <= 0:
                self.Set_StyleSheet.emit(F"time_T_n_{i+1}", "color: #0000FF")

    def time_Temperature_Time(self):
        hour = dt.datetime.now().hour
        for i in range(1, 8):
            self.Set_Text.emit(F"time_T_{i}", str((hour+i)-24 if hour+i > 23 else hour+i)+":00")
            self.Set_Text.emit(F"time_T_n_{i}", str(int(round(self.k2c(self.data["hourly"][i]["temp"]),0)))+"'C")
