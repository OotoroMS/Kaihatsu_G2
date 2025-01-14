#外観検査部の動作確認画面
from BaseFrame import BaseFrame
from Button import Button

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

MAINTITLE="GUI_option_test\\image\\title\\pic64.png"
#   メイン画面描画・処理クラス
class Test02Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 200, 400, 650, 320, "GUI_option_test\\image\\button\\pic45.png", self.try06),#ソレノイド前進
            Button(self.screen, 1000, 400, 650, 320, "GUI_option_test\\image\\button\\pic46.png", self.try07),#ステッピングモータ回転
            Button(self.screen, 0, 960, 300, 120, "GUI_option_test\\image\\button\\back.png", self.move_motiontest)
        }
    
        #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()

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