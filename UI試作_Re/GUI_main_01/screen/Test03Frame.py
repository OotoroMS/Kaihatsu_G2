#移動部の動作確認画面
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from filepath import *
from parts.Lamp import Lamp
import pygame
from parts.ButtonAtLamp import ButtonAtLamp
import time

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

MAINTITLE=IMAGEFILEPATH + "title\\pic65.png"#寸法･分別部
#   メイン画面描画・処理クラス
class Test03Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 20, 490, 360, 250, IMAGEFILEPATH + "button\\pic51.png", self.deset),#デジタルインジケータ基準値変更
            Button(self.screen, 500, 190, 550, 250, IMAGEFILEPATH + "button\\pic52.png", self.try11),#寸法壁押出シリンダ前進
            Button(self.screen, 0, 960, 300, 120, IMAGEFILEPATH + "button\\back.png", self.move_motiontest)#戻る
        }
        self.lamp_buttons = {
            ButtonAtLamp(self.screen, 500, 490, 550, 250, IMAGEFILEPATH + "button\\pic56.png", self.try12),#寸法上下シリンダ上昇
            ButtonAtLamp(self.screen, 1150, 490, 550, 250, IMAGEFILEPATH + "button\\pic57.png", self.try13),#寸法上下シリンダ下降
            ButtonAtLamp(self.screen, 500, 790, 550, 250, IMAGEFILEPATH + "button\\pic54.png", self.try14)#分別押出シリンダ前進
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1150, 200, 550, 240, IMAGEFILEPATH + "button\\pic53.png"),#寸法壁押出シリンダ後退
            Picture(self.screen, 1150, 800, 550, 240, IMAGEFILEPATH + "button\\pic55.png")#分別押出シリンダ後退
        }
        self.lamps = list((
            Lamp(self.screen, 1590, 290,60,60, GRAY),#寸法壁押出シリンダ後退
            Lamp(self.screen, 1590, 890,60,60, GRAY)#分別押出シリンダ後退
        ))
    
        #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        for button in self.lamp_buttons:
            button.draw()
        for lamp in self.lamps:
            lamp.draw()

    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.lamp_button_clicked(event)
                move = self.button_clicked(event)
                if move:
                    return move       
            return move
            

    def button_clicked(self, event):
        click_result = None
        for button in self.buttons:
            click_result = button.is_clicked(event)
            if click_result:
                return click_result
        return click_result

    def lamp_button_clicked(self, event):
        click_result = False
        for button in self.lamp_buttons:
            click_result = button.is_clicked(event)
            if click_result:
                print("try start")
                button.update_lamp_color("GREEN")
                button.draw()
                pygame.display.update()
                time.sleep(5)
                button.update_lamp_color("YEROW")
                button.draw()
                pygame.display.update()
                pygame.time.delay(5000)
                button.update_lamp_color("GRAY")
                button.draw()
                pygame.display.update()
                print("try end")

    def change_color(self):
        if self.color == YEROW:
            self.color = GREEN
        else:
            self.color = YEROW
        
        self.lamps[0].update_color(self.color)


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