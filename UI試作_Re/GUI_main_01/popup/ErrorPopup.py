# エラーポップアップ
import pygame
from typing import Tuple, Optional
from popup.CaluclatePopup import *
from popup.BasePopup import BasePopup
from parts.Picture import Picture
from filepath import *

GRAY = ((200,200,200))      #   カラーコード(灰色)
BLACK = ((255,255,255))     #   カラーコード(黒)
WHITE = ((0,0,0))           #   カラーコード(白)
BACKFRAME = IMAGEFILEPATH+"button\\back.png"
ERRORMASAGE = "エラーが発生しました"
PLACETEXT   = "投入部"
ERRORIMAGE  = IMAGEFILEPATH + "exptxt\\error.png"
IMAGESIZE   = (400,300)

class ErrorPopup(BasePopup):
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font):
        super().__init__(screen, font, "")
        self.message_font = pygame.font.Font(font, 100)
        self.maintext  = ERRORMASAGE
        self.codetext  = "エラー001"
        self.placetext = PLACETEXT
        self.maintext_message  = self.message_font.render(self.maintext,  True, WHITE)
        self.codetext_message  = self.message_font.render(self.codetext,  True, WHITE)
        self.placetext_message = self.message_font.render(self.placetext, True, WHITE)
        text_width  = self.maintext_message.get_width()
        text_height = self.maintext_message.get_height()
        image_x = self.pos_x + (self.width  - text_width)// 2 - IMAGESIZE[0] * 0.8
        image_y = self.pos_y + text_height
        self.image = Picture(self.screen, image_x, image_y, IMAGESIZE[0], IMAGESIZE[1], ERRORIMAGE)

    def draw(self):
        """
        画面更新処理。
        """
        if self.rect:
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)
            text_width  = self.maintext_message.get_width()
            text_height = self.maintext_message.get_height()
            maintext_y  = text_height + self.pos_y
            code_width  = self.codetext_message.get_width()
            code_y      = maintext_y + text_height
            place_width = self.placetext_message.get_width()
            place_y     = code_y + text_height
            self.screen.blit(self.maintext_message,    (((self.pos_x + (self.width  - text_width)// 2),  maintext_y)))
            self.screen.blit(self.codetext_message,    (((self.pos_x + (self.width  - code_width)// 2),  code_y)))
            self.screen.blit(self.placetext_message,   (((self.pos_x + (self.width - place_width)// 2),  place_y)))
            for button in self.buttons:
                button.draw()
            self.image.draw()
        else:
            print("失敗")
        
    def update_error_masage(self, vaital, place):
        self.codetext = vaital
        self.placetext = place
        self.codetext_message = self.message_font.render(self.codetext, True, WHITE)
        self.placetext_message   = self.message_font.render(self.placetext, True, WHITE)