# 遷移警告ポップアップ
import pygame
from typing import Tuple, Optional
from pygame.font import Font
from popup.CaluclatePopup import *
from popup.BasePopup import BasePopup
from parts.Picture import Picture
from filepath import *

WHITE          = ((0,0,0))           #   カラーコード(白)
GRAY           = ((200,200,200))      #   カラーコード(灰色)
BLACK          = ((255,255,255))     #   カラーコード(黒)
IMAGESIZE      = (250, 150)
IMAGEDISTANSE  = 50
TEXTDISTANSE   = 200
BACKFRAME      = IMAGEFILEPATH + "button\\back.png"
WORNINGIMAGE   = IMAGEFILEPATH + "exptxt\\warning.png"
DISPLAYTEXT_01 = "動作確認画面に移行するには"
DISPLAYTEXT_02 = "装置が停止中であることを"
DISPLAYTEXT_03 = "確認してください"

class WorningPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, font: Font):
        super().__init__(screen, font, "")
        self.message_font = pygame.font.Font(font, 100)
        self.text_top     = self.message_font.render(DISPLAYTEXT_01, True, WHITE)
        self.text_middle  = self.message_font.render(DISPLAYTEXT_02, True, WHITE)
        self.text_bottom  = self.message_font.render(DISPLAYTEXT_03, True, WHITE)
        image_x           = self.pos_x + (self.width // 2) -  (IMAGESIZE[0] // 2)
        image_y           = self.pos_y + 25
        self.image = Picture(self.screen, image_x, image_y, IMAGESIZE[0], IMAGESIZE[1], WORNINGIMAGE)

    # 画面全体の描画
    def draw(self):
        pygame.draw.rect(self.screen, GRAY,  self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)
        self.text_draw()
        for button in self.buttons:
            button.draw()
        self.image.draw()

    # テキストの描画処理
    def text_draw(self):
        text_top_width  = self.text_top.get_width()     
        text_top_height = self.text_top.get_height()
        text_top_y      = self.pos_y + TEXTDISTANSE              # text_topのy座標
        
        text_middle_width  = self.text_middle.get_width()
        text_middle_height = self.text_middle.get_height()
        text_middle_y      = text_top_y + text_top_height        # text_middleのy座標

        text_bottom_width = self.text_bottom.get_width()
        text_bottom_y     = text_middle_y + text_middle_height   # text_bottomの座標

        # (self.pos_x + (self.width - text_width) // 2)でテキストをポップアップの中央に設定している
        self.screen.blit(self.text_top,    ((self.pos_x + (self.width - text_top_width)     // 2),  text_top_y))
        self.screen.blit(self.text_middle, ((self.pos_x + (self.width - text_middle_width)  // 2),  text_middle_y))
        self.screen.blit(self.text_bottom, ((self.pos_x + (self.width -  text_bottom_width) // 2),  text_bottom_y))
