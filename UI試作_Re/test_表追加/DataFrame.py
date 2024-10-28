import pygame
from pygame.locals import *
from BaseFrame import BaseFrame
from Button import Button

BRACK = ((0,0,0))
WHITE = ((255,255,255))

#   データ一覧
class DataFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen)
        self.font = pygame.font.Font(font, 60)
        self.title_text = self.font.render("データ一覧", True, BRACK)
        #   ボタンクラス
        self.buttons = {
            0   : Button(self.screen, 150, 200, 700, 300, WHITE, "良否カウント", 90, self.move_count),
            1   : Button(self.screen, 150, 550, 700, 300, WHITE, "寸法検査ログ", 90, self.move_graph),
            2   : Button(self.screen, 1570, 930, 300, 100, WHITE, "戻る", 90, self.move_main)
        }

    #   イベント処理を記述
    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.buttons:
                    move = self.buttons[i].is_clicked(event)
                    if move:
                        break
                return move
    
    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        #self.screen.fill((255,255,255))
        self.screen.blit(self.title_text,(200,50))
        for i in self.buttons:
            self.buttons[i].draw()
        pygame.display.flip()

    #   良否カウント画面に遷移
    def move_count(self):
        print("return: count")
        return "count"

    #   寸法検査ログ画面に遷移
    def move_graph(self):
        print("return: graph")
        return "graph"

    #   メインメニューに遷移
    def move_main(self):
        return "main"