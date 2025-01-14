#ほとんどの画面作成の基礎
import pygame
from pygame.locals import *
from Button import Button
from Picture import Picture

BRACK = ((0,0,0))
GRAY  = ((200,200,200))
FONT = "GUI_option_test\\image\\button\\pic01.png"
BASETITLE="GUI_option_test\\image\\title\\pic03.png"

#このクラスを画面作成する際に引用し、必要な部分のみ変更する
class BaseFrame():
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, BASETITLE)#表示したい画像の設定(配置する座標、画像の大きさなどを記述する)
        }
        self.buttons = {
            Button(self.screen, 141, 50, 200, 100, FONT, self.test),#表示したいボタンの設定、ボタンを押下した際の動作も加える
            
        }
    #   イベント処理を記述
    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:#クリックがあった際の処理
                for button in self.buttons:
                    move = button.is_clicked(event)
                    if move:
                        break
                return move


    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:#配置場所がかぶってる場合、後に表示させたものが上にくるので順番に気をつける
            image.draw()
        for button in self.buttons:
            button.draw()
        

    def test(self):
        print("test")
