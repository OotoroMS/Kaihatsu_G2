#蓄積部の動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
from Lamp import Lamp

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

MAINTITLE="GUI_main_test\\image\\title\\pic66.png"
#   メイン画面描画・処理クラス
class Test04Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 1000, 510, 600, 280, "GUI_main_test\\image\\button\\pic60.png", self.try15),#上下シリンダ下降
            Button(self.screen, 0, 960, 300, 120, "GUI_main_test\\image\\button\\back.png", self.move_motiontest)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1000, 220, 600, 230, "GUI_main_test\\image\\button\\pic58.png"),#蓄積部センサ
            Picture(self.screen, 250, 520, 600, 260, "GUI_main_test\\image\\button\\pic59.png"),#上下シリンダ上昇
        }
        self.lamps = list((
            Lamp(self.screen, 1450, 300,60,60, GRAY),#蓄積部センサ
            Lamp(self.screen, 745, 620,60,60, GRAY),#上下シリンダ上昇
            Lamp(self.screen, 1495, 620,60,60, GRAY)#下降
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
    def try15(self):
        return "try15"
    
    def try16(self):
        return "try16" 

    def move_motiontest(self):
        return "motiontest"