# エラーポップアップ
import pygame
from typing import Tuple, Optional
from parts.CaluclatePopup import *
from popup.BasePopup import BasePopup
from parts.Picture import Picture
from constant.FilePath    import *

GRAY        = ((200,200,200))      #   カラーコード(灰色)
BLACK       = ((255,255,255))     #   カラーコード(黒)
WHITE       = ((0,0,0))           #   カラーコード(白)
IMAGE_SIZE   = (400,300)
BACK_BUTTON  = BUTTONFILEPATH + "back.png"
ERROR_IMAGE  = EXPTXTFILEPATH + "error.png"
ERROR_MASAGE = "エラーが発生しました"
ERROR_NUMBER = "エラー001"
PLACETEXT   = "投入部"

class ErrorPopup(BasePopup):
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font):
        super().__init__(screen, font, "")
        self.message_font = pygame.font.Font(font, 100)
        self.maintext  = ERROR_MASAGE
        self.codetext  = ERROR_NUMBER
        self.placetext = PLACETEXT
        self.maintext_message  = self.message_font.render(self.maintext,  True, WHITE)
        self.codetext_message  = self.message_font.render(self.codetext,  True, WHITE)
        self.placetext_message = self.message_font.render(self.placetext, True, WHITE)
        text_width  = self.maintext_message.get_width()
        text_height = self.maintext_message.get_height()
        image_x = self.pos_x + (self.width  - text_width)// 2 - IMAGE_SIZE[0] * 0.8
        image_y = self.pos_y + text_height
        self.image = Picture(self.screen, image_x, image_y, IMAGE_SIZE[0], IMAGE_SIZE[1], ERROR_IMAGE)

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