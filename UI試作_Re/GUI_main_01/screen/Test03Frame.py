#移動部の動作確認画面
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from filepath import *

MAINTITLE=IMAGEFILEPATH + "title\\pic65.png"
#   メイン画面描画・処理クラス
class Test03Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 20, 490, 360, 250, IMAGEFILEPATH + "button\\pic51.png", self.deset),
            Button(self.screen, 500, 190, 550, 250, IMAGEFILEPATH + "button\\pic52.png", self.try11),
            Button(self.screen, 500, 490, 550, 250, IMAGEFILEPATH + "button\\pic54.png", self.try12),
            Button(self.screen, 500, 790, 550, 250, IMAGEFILEPATH + "button\\pic56.png", self.try13),
            Button(self.screen, 1150, 790, 550, 250, IMAGEFILEPATH + "button\\pic57.png", self.try14),
            Button(self.screen, 0, 960, 300, 120, IMAGEFILEPATH + "button\\back.png", self.move_motiontest)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1150, 200, 550, 240, IMAGEFILEPATH + "button\\pic53.png"),
            Picture(self.screen, 1150, 500, 550, 240, IMAGEFILEPATH + "button\\pic55.png")
        }
    
    #   動作確認ボタン押下処理
    def deset(self):
        return "deset"
    
    def try11(self):
        return "try11"

    def try12(self):
        return "try12"
    
    def try13(self):
        return "try13"

    def try14(self):
        return "try14"    

    def move_motiontest(self):
        return "motiontest"