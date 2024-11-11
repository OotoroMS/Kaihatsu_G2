#寸法・分別部の動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
from Lamp import Lamp

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

MAINTITLE="GUI_main_test\\image\\title\\pic65.png"
#   メイン画面描画・処理クラス
class Test03Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 20, 490, 360, 250, "GUI_main_test\\image\\button\\pic51.png", self.deset),#デジタルインジケータ基準値変更
            Button(self.screen, 500, 190, 550, 250, "GUI_main_test\\image\\button\\pic52.png", self.try11),#寸法壁押出シリンダ前進
            Button(self.screen, 500, 490, 550, 250, "GUI_main_test\\image\\button\\pic54.png", self.try12),#分別押出シリンダ前進
            Button(self.screen, 500, 790, 550, 250, "GUI_main_test\\image\\button\\pic56.png", self.try13),#分別上下シリンダ上昇
            Button(self.screen, 1150, 790, 550, 250, "GUI_main_test\\image\\button\\pic57.png", self.try14),#下降
            Button(self.screen, 0, 960, 300, 120, "GUI_main_test\\image\\button\\back.png", self.move_motiontest)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1150, 200, 550, 240, "GUI_main_test\\image\\button\\pic53.png"),#寸法壁押出シリンダ後退
            Picture(self.screen, 1150, 500, 550, 240, "GUI_main_test\\image\\button\\pic55.png")#分別押出シリンダ後退
        }
    
        self.lamps = list((
            Lamp(self.screen, 1590, 290,60,60, GRAY),#寸法壁押出シリンダ後退
            Lamp(self.screen, 940, 585,60,60, GRAY),#分別押出シリンダ前進
            Lamp(self.screen, 1570, 590,60,60, GRAY),#分別押出シリンダ後退
            Lamp(self.screen, 945, 890,60,60, GRAY),#分別押出シリンダ前進
            Lamp(self.screen, 1590, 890,60,60, GRAY)#下降
        ))

    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        for lamp in self.lamps:
            lamp.draw()

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