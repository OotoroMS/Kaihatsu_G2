# 遷移警告ポップアップ
import pygame
from typing               import Tuple, Optional
from pygame.font          import Font
from parts.CaluclatePopup import *
from popup.BasePopup      import BasePopup
from parts.Picture        import Picture
from constant.FilePath    import *

WHITE          = ((0,0,0))           #   カラーコード(白)
GRAY           = ((200,200,200))      #   カラーコード(灰色)
BLACK          = ((255,255,255))     #   カラーコード(黒)
IMAGESIZE      = (250, 150)
IMAGEDISTANSE  = 50
TEXTDISTANSE   = 200
BACKFRAME      = BUTTONFILEPATH + "back.png"
WORNINGIMAGE   = EXPTXTFILEPATH + "warning.png"
DISPLAYTEXT_01 = "動作確認画面に移行するには"
DISPLAYTEXT_02 = "装置が停止中であることを"
DISPLAYTEXT_03 = "確認してください"

class WorningPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, font: Font):
        super().__init__(screen, font, "")
        self.message_font = pygame.font.Font(font, 100)
        self.top_text     = self.message_font.render(DISPLAYTEXT_01, True, WHITE)
        self.middle_text  = self.message_font.render(DISPLAYTEXT_02, True, WHITE)
        self.bottom_text  = self.message_font.render(DISPLAYTEXT_03, True, WHITE)
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
        top_text_width  = self.top_text.get_width()     
        top_text_height = self.top_text.get_height()
        top_text_y      = self.pos_y + TEXTDISTANSE              # text_topのy座標
        
        middle_text_width  = self.middle_text.get_width()
        middle_text_height = self.middle_text.get_height()
        middle_text_y      = top_text_y + top_text_height        # text_middleのy座標

        bottom_text_width = self.bottom_text.get_width()
        bottom_text_y     = middle_text_y + middle_text_height   # text_bottomの座標

        # (self.pos_x + (self.width - text_width) // 2)でテキストをポップアップの中央に設定している
        self.screen.blit(self.top_text,    ((self.pos_x + (self.width - top_text_width)     // 2),  top_text_y))
        self.screen.blit(self.middle_text, ((self.pos_x + (self.width - middle_text_width)  // 2),  middle_text_y))
        self.screen.blit(self.bottom_text, ((self.pos_x + (self.width -  bottom_text_width) // 2),  bottom_text_y))
