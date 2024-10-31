import pygame
from pygame.locals import *
from Button import Button

BRACK = ((0,0,0))
GRAY  = ((200,200,200))
FONT = "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\data.png"

class BaseFrame():
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font
        self.font_title = pygame.font.Font(self.font, 60)
        self.text_title = self.font_title.render("テスト", True, BRACK)
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
        self.screen.blit(self.text_title,(200,10))
        for button in self.buttons:
            button.draw()

    def test(self):
        print("test")
