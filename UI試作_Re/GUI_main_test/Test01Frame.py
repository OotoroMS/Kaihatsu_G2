#投入･洗浄部の動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
from Lamp import Lamp

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

COLOR = ((GRAY))
MAINTITLE="GUI_main_test\\image\\title\\pic63.png"
#   メイン画面描画・処理クラス
class Test01Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 1100, 190, 550, 250, "GUI_main_test\\image\\button\\pic40.png", self.try01),#偏心モータ回転
            Button(self.screen, 350, 490, 550, 250, "GUI_main_test\\image\\button\\pic41.png", self.try02),#押出シリンダ前進
            Button(self.screen, 1100, 490, 550, 250, "GUI_main_test\\image\\button\\pic42.png", self.try03),#押出シリンダ後退
            Button(self.screen, 350, 790, 550, 250, "GUI_main_test\\image\\button\\pic43.png", self.try04),#ポンプ
            Button(self.screen, 1100, 790, 550, 250, "GUI_main_test\\image\\button\\pic44.png", self.try05),#エアブロー
            Button(self.screen, 0, 960, 300, 120, "GUI_main_test\\image\\button\\back.png", self.move_motiontest)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 50, 220, 400, 200, "GUI_main_test\\image\\button\\pic38.png"),#引っかかり検知
            Picture(self.screen, 500, 220, 400, 200, "GUI_main_test\\image\\button\\pic39.png")#ワーク検知
        }
        self.lamps = list((
            Lamp(self.screen, 380, 295,50,50, GRAY),#引っかかり検知
            Lamp(self.screen, 820, 295,50,50, GRAY),#ワーク検知
            Lamp(self.screen, 800, 580,60,60, GRAY),#押出シリンダ前進
            Lamp(self.screen, 1550, 580,60,60, GRAY)#押出シリンダ後退
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

    def change_color(self):
        if self.color == YEROW:
            self.color = GREEN
        else:
            self.color = YEROW
        
        self.lamps[0].update_color(self.color)

    #   動作確認ボタン押下処理
    def try01(self):
        return "try01"
    
    def try02(self):
        return "try02"

    def try03(self):
        return "try03"
    
    def try04(self):
        return "try04"

    def try05(self):
        return "try05"    

    def move_motiontest(self):
        return "motiontest"