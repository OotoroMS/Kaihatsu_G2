#投入･洗浄部の動作確認画面
import pygame
from screen.BaseFrame import BaseFrame
from parts.ButtonAtLamp import ButtonAtLamp
from parts.Button       import Button
from parts.Picture import Picture
from parts.Lamp import Lamp
import time
from filepath import *
BLACK = ((0,0,0))
GRAY  = ((200,200,200))
YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

COLOR = ((GRAY))
MAINTITLE=IMAGEFILEPATH + "title\\pic63.png"
#   メイン画面描画・処理クラス
class Test01Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 0, 960, 300, 120, IMAGEFILEPATH + "button\\back.png", self.move_motiontest)
        }
        self.lamp_buttons = {
            ButtonAtLamp(self.screen, 1100, 190, 550, 250, IMAGEFILEPATH + "button\\pic40.png", self.try01),
            ButtonAtLamp(self.screen, 350, 490, 550, 250, IMAGEFILEPATH + "button\\pic41.png", self.try02),
            ButtonAtLamp(self.screen, 1100, 490, 550, 250, IMAGEFILEPATH + "button\\pic42.png", self.try03),
            ButtonAtLamp(self.screen, 350, 790, 550, 250, IMAGEFILEPATH + "button\\pic43.png", self.try04),
            ButtonAtLamp(self.screen, 1100, 790, 550, 250, IMAGEFILEPATH + "button\\pic44.png", self.try05)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 50, 220, 400, 200, IMAGEFILEPATH + "button\\pic38.png"),
            Picture(self.screen, 500, 220, 400, 200, IMAGEFILEPATH + "button\\pic39.png")
        }
        self.lamps = list((
            Lamp(self.screen, 380, 295,50,50, GRAY),
            Lamp(self.screen, 825, 295,50,50, GRAY)
        ))
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
    def try01(self):
        return True
    
    def try02(self):
        return True

    def try03(self):
        return True
    
    def try04(self):
        return True

    def try05(self):
        return True   

    def move_motiontest(self):
        return "motiontest"