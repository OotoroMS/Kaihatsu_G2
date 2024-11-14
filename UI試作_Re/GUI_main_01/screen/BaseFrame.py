import pygame
from pygame.locals import *
from parts.Button import Button
from parts.Picture import Picture
from filepath import *

BRACK = ((0,0,0))
GRAY  = ((200,200,200))
FONT = IMAGEFILEPATH + "button\\pic01.png"
BASETITLE= IMAGEFILEPATH + "title\\pic03.png"

class BaseFrame():
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, BASETITLE)
        }
        self.buttons = {
            Button(self.screen, 141, 50, 200, 100, FONT, self.test),
            
        }
    #   イベント処理を記述
    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    move = button.is_clicked(event)
                    if move:
                        break
                return move


    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        

    def test(self):
        print("test")
