#移動部の動作確認画面
from screen.BaseScreen   import BaseFrame
from parts.Button        import Button
from parts.Picture       import Picture
from parts.ButtonAtLamp  import ButtonAtLamp as LampButton
from parts.Lamp          import Lamp
from constant.FilePath   import *
from constant.ScreenName import *
import pygame
RED = ((255,0,0))
BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YELLOW = ((255,255,0)) 
GREEN = ((0,255,0))
LIGHTBLUE=((176,196,222))

COLOR = ((GRAY))
MAINTITLE=TITLEFILEPATH  + "pic63.png"
#   メイン画面描画・処理クラス
class Test01Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 160, 350, 400, 200, BUTTONFILEPATH + "pic38.png", self.try01),#モータ正転
            Button(self.screen, 750, 350, 400, 200, BUTTONFILEPATH + "pic39.png", self.try02),#逆転
            Button(self.screen, 750, 850, 550, 200, BUTTONFILEPATH + "pic44.png", self.try05),#吸着ON
            Button(self.screen, 0, 960, 300, 120,   BUTTONFILEPATH + "back.png", self.move_motiontest)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 90,180,1150,400, EXPTXTFILEPATH + "pic76.png"),#背景の水色
            Picture(self.screen, 1350, 360, 400, 170, EXPTXTFILEPATH + "pic40.png"),#入口ワーク検知
            Picture(self.screen, 1350, 610, 400, 170, EXPTXTFILEPATH + "pic43.png")#出口ワーク検知
        }
        self.lamp_buttons = [
            LampButton(self.screen, 160, 600, 550, 200, BUTTONFILEPATH + "pic41.png", self.try03),#上下シリンダ上昇
            LampButton(self.screen, 750, 600, 550, 200, BUTTONFILEPATH + "pic42.png", self.try04),#下降
        ]
        self.lamps = list((
            Lamp(self.screen, 240, 220,70,70, RED),#モーター
            Lamp(self.screen, 390, 220,70,70, YELLOW),
            Lamp(self.screen, 540, 220,70,70, YELLOW),
            Lamp(self.screen, 690, 220,70,70, YELLOW),
            Lamp(self.screen, 840, 220,70,70, YELLOW),
            Lamp(self.screen, 990, 220,70,70, RED),#モーター
            Lamp(self.screen, 1680, 420,50,50, YELLOW),#入口ワーク検知
            Lamp(self.screen, 1680, 670,50,50, YELLOW)#出口ワーク検知
        ))
        self.color = GRAY

    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        #pygame.draw.rect(self.screen,LIGHTBLUE,(90,180,1150,400))
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        for button in self.lamp_buttons:
            button.draw()
        for lamp in self.lamps:
            lamp.draw()

    # def change_color(self):
    #     if self.color == YELLOW:
    #         self.color = GREEN
    #     else:
    #         self.color = YELLOW
        
    #     self.lamps[0].update_color(self.color)

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