#移動部の動作確認画面
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from parts.Lamp import Lamp
from filepath import *
import pygame
from parts.ButtonAtLamp import ButtonAtLamp
import time


BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

MAINTITLE=IMAGEFILEPATH + "title\\pic64.png"#移動部
#   メイン画面描画・処理クラス
class Test02Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 350, 190, 550, 250, IMAGEFILEPATH + "button\\pic45.png", self.try06),#吸着ON
            Button(self.screen, 0, 960, 300, 120, IMAGEFILEPATH + "button\\back.png", self.move_motiontest)#戻る
        }
        self.lamp_buttons = {
            ButtonAtLamp(self.screen, 350, 490, 550, 250, IMAGEFILEPATH + "button\\pic47.png", self.try07),#上下シリンダ上昇
            ButtonAtLamp(self.screen, 1100, 490, 550, 250, IMAGEFILEPATH + "button\\pic48.png", self.try08),#下降
            ButtonAtLamp(self.screen, 350, 790, 550, 250, IMAGEFILEPATH + "button\\pic49.png", self.try09),#移動モータ正転
            ButtonAtLamp(self.screen, 1100, 790, 550, 250, IMAGEFILEPATH + "button\\pic50.png", self.try10),#逆転
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1100, 200, 550, 240, IMAGEFILEPATH + "button\\pic46.png")#移動中ワーク検知
        }
        self.lamps = [
            Lamp(self.screen, 1540, 290,60,60, GRAY)#移動中ワーク検知
        ]
        self.color = GRAY
    
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