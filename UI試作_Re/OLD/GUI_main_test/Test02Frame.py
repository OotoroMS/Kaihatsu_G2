#移動部の動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
from Lamp import Lamp

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

MAINTITLE="GUI_main_test\\image\\title\\pic64.png"
#   メイン画面描画・処理クラス
class Test02Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 350, 190, 550, 250, "GUI_main_test\\image\\button\\pic45.png", self.try06),#吸着ON
            Button(self.screen, 350, 490, 550, 250, "GUI_main_test\\image\\button\\pic47.png", self.try07),#上下シリンダ上昇
            Button(self.screen, 1100, 490, 550, 250, "GUI_main_test\\image\\button\\pic48.png", self.try08),#下降
            Button(self.screen, 350, 790, 550, 250, "GUI_main_test\\image\\button\\pic49.png", self.try09),#移動モータ正転
            Button(self.screen, 1100, 790, 550, 250, "GUI_main_test\\image\\button\\pic50.png", self.try10),#逆転
            Button(self.screen, 0, 960, 300, 120, "GUI_main_test\\image\\button\\back.png", self.move_motiontest)#戻る
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1100, 200, 550, 240, "GUI_main_test\\image\\button\\pic46.png")#移動中ワーク検知
        }
        self.lamps = list((
            Lamp(self.screen, 1540, 290,60,60, GRAY),#移動中ワーク検知
            Lamp(self.screen, 800, 585,60,60, GRAY),#上下シリンダ上昇
            Lamp(self.screen, 1550, 585,60,60, GRAY),#下降
            Lamp(self.screen, 780, 880,60,60, GRAY),#移動モータ正転
            Lamp(self.screen, 1530, 880,60,60, GRAY)#逆転
        ))
        self.color = GRAY
    
        #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        for lamp in self.lamps:
            lamp.draw()


    #   動作確認ボタン押下処理
    def try06(self):
        return "try06"
    
    def try07(self):
        return "try07"

    def try08(self):
        return "try08"
    
    def try09(self):
        return "try09"

    def try10(self):
        return "try10"    

    def move_motiontest(self):
        return "motiontest"