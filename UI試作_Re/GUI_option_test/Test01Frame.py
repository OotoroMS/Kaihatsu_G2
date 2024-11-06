#移動部の動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
from Lamp import Lamp
import pygame
RED = ((255,0,0))
BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YELLOW = ((255,255,0)) 
GREEN = ((0,255,0))
LIGHTBLUE=((176,196,222))

COLOR = ((GRAY))
MAINTITLE="GUI_option_test\\image\\title\\pic63.png"
#   メイン画面描画・処理クラス
class Test01Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 160, 350, 400, 200, "GUI_option_test\\image\\button\\pic38.png", self.try01),
            Button(self.screen, 750, 350, 400, 200, "GUI_option_test\\image\\button\\pic39.png", self.try02),
            Button(self.screen, 160, 600, 550, 200, "GUI_option_test\\image\\button\\pic41.png", self.try03),
            Button(self.screen, 750, 600, 550, 200, "GUI_option_test\\image\\button\\pic42.png", self.try04),
            Button(self.screen, 750, 850, 550, 200, "GUI_option_test\\image\\button\\pic44.png", self.try05),
            Button(self.screen, 0, 960, 300, 120, "GUI_option_test\\image\\button\\back.png", self.move_motiontest)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 90,180,1150,400, "GUI_option_test\\image\\exptxt\\pic76.png"),
            Picture(self.screen, 1350, 360, 400, 170, "GUI_option_test\\image\\exptxt\\pic40.png"),
            Picture(self.screen, 1350, 610, 400, 170, "GUI_option_test\\image\\exptxt\\pic43.png")
        }
        self.lamps = list((
            Lamp(self.screen, 240, 220,70,70, RED),
            Lamp(self.screen, 390, 220,70,70, YELLOW),
            Lamp(self.screen, 540, 220,70,70, YELLOW),
            Lamp(self.screen, 690, 220,70,70, YELLOW),
            Lamp(self.screen, 840, 220,70,70, YELLOW),
            Lamp(self.screen, 990, 220,70,70, RED)
        ))
        self.color = GRAY

    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        #pygame.draw.rect(self.screen,LIGHTBLUE,(90,180,1150,400))
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        for lamp in self.lamps:
            lamp.draw()

    def change_color(self):
        if self.color == YELLOW:
            self.color = GREEN
        else:
            self.color = YELLOW
        
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