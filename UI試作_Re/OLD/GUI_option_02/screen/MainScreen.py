#メインメニュー
from screen.BaseScreen import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from constant.FilePath   import *
from constant.ScreenName import *

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
MAINTITLE=TITLEFILEPATH  + "pic03.png"
#   メイン画面描画・処理クラス
class MainFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 150, 300, 700, 350,BUTTONFILEPATH + "pic01.png", self.move_data),
            Button(self.screen, 1000, 300, 700, 350,BUTTONFILEPATH + "pic02.png", self.move_pass),
            Button(self.screen, 0, 960, 330, 120,BUTTONFILEPATH + "pic04.png", self.end_app)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 175, 600, 650, 350, EXPTXTFILEPATH + "pic67.png"),
            Picture(self.screen, 1025, 600, 650, 350, EXPTXTFILEPATH + "pic68.png")
        }
    
    #   データ一覧ボタン押下処理
    def move_data(self):
        print("return data")
        return "data"
    
        #   動作確認ボタン押下処理
    def move_pass(self):
        print("return pass")
        return "pass"
    
    def end_app(self):
        print("return end")
        return "end"