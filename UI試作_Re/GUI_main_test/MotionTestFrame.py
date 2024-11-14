#動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
import pygame

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
RED  = ((255,0,0))#RGB
GREEN  = ((0,255,0))
BLUE  = ((0,0,255))
YELLOW  = ((255,255,0))
MAINTITLE="GUI_main_test\\image\\title\\pic62.png"
#   メイン画面描画・処理クラス
class MotionTestFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 50, 650, 330, 150, "GUI_main_test\\image\\button\\pic33.png", self.move_test01),#投入･洗浄部
            Button(self.screen, 570, 170, 330, 150, "GUI_main_test\\image\\button\\pic34.png", self.move_test02),#移動部
            Button(self.screen, 670, 850, 330, 150, "GUI_main_test\\image\\button\\pic35.png", self.move_test03),#寸法･分別部
            Button(self.screen, 1100, 270, 330, 150, "GUI_main_test\\image\\button\\pic36.png", self.move_test04),#蓄積部
            Button(self.screen, 1570, 710, 330, 150, "GUI_main_test\\image\\button\\pic74.png", self.dbreset),#DBリセット
            Button(self.screen, 1570, 900, 330, 150, "GUI_main_test\\image\\button\\pic37.png", self.move_changepass),#パスワード変更
            Button(self.screen, 0, 960, 330, 120, "GUI_main_test\\image\\button\\back.png", self.move_main)#戻る
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 250, 210, 1300, 740, "GUI_main_test\\image\\exptxt\\pic32.png")#装置の3D図
        }

    def draw(self):
        for image in self.images:
            image.draw()
        pygame.draw.line(self.screen,RED,(215,680),(400,560),8)#01
        pygame.draw.line(self.screen,YELLOW,(750,260),(660,410),8)#02
        pygame.draw.line(self.screen,GREEN,(880,950),(780,670),8)#03
        pygame.draw.line(self.screen,BLUE,(1260,410),(1000,550),8)#04
        for button in self.buttons:
            button.draw()

    #   動作確認ボタン押下処理
    def move_test01(self):
        return "test01"
    
    def move_test02(self):
        return "test02"

    def move_test03(self):
        return "test03"
    
    def move_test04(self):
        return "test04"
    #データベースリセット
    def dbreset(self):
        return "dbreset"    
    #パスワード変更
    def move_changepass(self):
        return "changepass"
    #メインメニューに戻る
    def move_main(self):
        return "main"