import cv2
from PyQt5 import QtGui


class number_img:
    def __init__(self):
        for i in range(0,10):
            setattr(self, 'number' + str(i), self.imgprocess(cv2.imread('img/number/'+ str(i)+'.png', cv2.IMREAD_UNCHANGED)))

    def imgprocess(self,img):
        self.hh, self.ww, self.cc = img.shape
        return self.img2bit(img,self.hh,self.ww)

    def img2bit(self,img,h,w):
        for i in range(0,h):
            for o in range(0,w):
                if img[i][o][3] != 0 and img[i][o][1] >= 100:
                    img[i][o] = [110, 110, 110, 110]
                elif img[i][o][3] != 0 and img[i][o][1] == 0:
                    img[i][o] = [255,255,255,255]
        return img

    def coalescence(self, img1, img2):
        return cv2.hconcat([getattr(self, 'number' + str(img1), lambda: 'default'), getattr(self, 'number' + str(img2), lambda: 'default')])

    def nm(self, img):
        self.img_conver = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        self.h, self.w, self.c = self.img_conver.shape

        self.img_conver = QtGui.QImage(self.img_conver, self.w, self.h, self.w * self.c, QtGui.QImage.Format_RGBA8888)
        return QtGui.QPixmap(self.img_conver)

    def printing(self, number):
        return self.nm(self.coalescence(int(number%100/10),int(number%10/1)))