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
MAINTITLE="GUI_option_test\\image\\title\\pic62.png"
#   メイン画面描画・処理クラス
class MotionTestFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 500, 830, 330, 150, "GUI_option_test\\image\\button\\pic33.png", self.move_test01),
            Button(self.screen, 950, 830, 330, 150, "GUI_option_test\\image\\button\\pic34.png", self.move_test02),
            Button(self.screen, 1570, 510, 330, 150, "GUI_option_test\\image\\button\\pic35.png",None),
            Button(self.screen, 1570, 710, 330, 150, "GUI_option_test\\image\\button\\pic74.png", self.dbreset),
            Button(self.screen, 1570, 900, 330, 150, "GUI_option_test\\image\\button\\pic37.png", self.move_changepass),
            Button(self.screen, 0, 960, 330, 120, "GUI_option_test\\image\\button\\back.png", self.move_main)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 180, 200, 1300, 740, "GUI_option_test\\image\\exptxt\\pic32.png")
        }

    def draw(self):
        for image in self.images:
            image.draw()
        pygame.draw.line(self.screen,RED,(665,850),(1040,500),8)#01
        pygame.draw.line(self.screen,BLUE,(1115,850),(1200,600),8)#02
        for button in self.buttons:
            button.draw()

    #   動作確認ボタン押下処理
    def move_test01(self):
        return "test01"
    
    def move_test02(self):
        return "test02"

    def dbreset(self):
        return "dbreset"    

    def move_changepass(self):
        return "changepass"

    def move_main(self):
        return "main"