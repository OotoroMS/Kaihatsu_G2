import pygame
from pygame.locals import *
from BaseFrame import BaseFrame
from Button import Button

BRACK = ((0,0,0))
WHITE = ((255,255,255))

#   メインメニュー
class MainFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen)
        #   タイトル
        self.font = pygame.font.Font(font, 60)
        self.title_text = self.font.render("検査・蓄積収納装置", True, BRACK)
        #   ボタンクラス
        self.buttons = {
            0   : Button(self.screen, 150, 200, 700, 300, WHITE, "データ一覧", 90, self.move_data),
            1   : Button(self.screen, 150, 550, 700, 300, WHITE, "メンテナンス", 90, self.move_mente),
            2   : Button(self.screen, 1570, 930, 300, 100, WHITE, "終了", 90, self.end_app)
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
    
    #   データ一覧画面に遷移
    def move_data(self):
        return "data"

    #   メンテナンス(パスワード入力)画面に遷移
    def move_mente(self):
        print("return: pass")
        return "pass"

    #   終了処理
    def end_app(self):
        print("return: end")
        return "end"