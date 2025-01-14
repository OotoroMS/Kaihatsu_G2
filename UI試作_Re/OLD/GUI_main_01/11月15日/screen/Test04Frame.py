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

MAINTITLE=IMAGEFILEPATH + "title\\pic66.png"#蓄積部
#   メイン画面描画・処理クラス
class Test04Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 0, 960, 300, 120, IMAGEFILEPATH + "button\\back.png", self.move_motiontest)#戻る
        }
        self.lamp_buttons = {
            ButtonAtLamp(self.screen, 1000, 510, 600, 280, IMAGEFILEPATH + "button\\pic60.png", self.try16)#上下シリンダ下降
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1000, 220, 600, 240, IMAGEFILEPATH + "button\\pic58.png"),#蓄積部センサ
            Picture(self.screen, 250, 520, 600, 260, IMAGEFILEPATH + "button\\pic59.png")#上下シリンダ上昇
        }
        self.lamps = list((
            Lamp(self.screen, 1490, 300,60,60, GRAY),#蓄積部センサ
            Lamp(self.screen, 745, 620,60,60, GRAY)#上下シリンダ上昇
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
    def try15(self):
        return "try15"
    
    def try16(self):
        return "try16" 

    def move_motiontest(self):
        return "motiontest"