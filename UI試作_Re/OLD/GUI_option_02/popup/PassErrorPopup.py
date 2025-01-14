# パスワード入力ミス伝達用ポップアップ
import pygame
from typing import Tuple, Optional

from pygame.font            import Font
from parts.CaluclatePopup   import *
from popup.BasePopup        import BasePopup
from parts.Picture          import Picture
from constant.FilePath      import *
from constant.PopupName     import *

WHITE          = ((0,0,0))           #   カラーコード(白)
GRAY           = ((200,200,200))      #   カラーコード(灰色)
BLACK          = ((255,255,255))     #   カラーコード(黒)
IMAGESIZE      = (550, 300)
IMAGEDISTANSE  = 50
TEXTDISTANSE   = 320
BACKFRAME      = BUTTONFILEPATH + "back.png"
FAILIMAGE      = EXPTXTFILEPATH + "pic78.png"
MAINTEXT       = "パスワードが違います"
RETRYTEXT      = "もう一度入力してください"
RESETTEXT      = "最初からやり直してください"

class PassErrorPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, font: Font, veiw_type : str):
        super().__init__(screen, font,"")
        self.message_font = pygame.font.Font(font, 100)
        self.main_text = self.message_font.render(MAINTEXT, True, WHITE)
        if veiw_type == NOT_PASS:
            self.sub_text = self.message_font.render(RETRYTEXT, True, WHITE)
        elif veiw_type == DIFFER_PASS:
            self.sub_text = self.message_font.render(RESETTEXT, True, WHITE)
        else:
            self.sub_text = self.message_font.render(RETRYTEXT, True, WHITE)

        image_x = self.pos_x + (self.width // 2) - (IMAGESIZE[0] // 2)
        image_y = self.pos_y + 25
        self.image = Picture(self.screen, image_x, image_y, IMAGESIZE[0], IMAGESIZE[1], FAILIMAGE)

    def draw(self):
        pygame.draw.rect(self.screen, GRAY,  self.rect)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2)
        self.text_draw()
        for button in self.buttons:
            button.draw()
        self.image.draw()

    # テキストの描画処理
    def text_draw(self):
        main_text_width  = self.main_text.get_width()
        main_text_height = self.main_text.get_height()
        main_text_y      = self.pos_y + TEXTDISTANSE

        sub_text_width = self.sub_text.get_width()
        sub_text_y     = main_text_height + main_text_y

        self.screen.blit(self.main_text, ((self.pos_x + (self.width - main_text_width) // 2), main_text_y))
        self.screen.blit(self.sub_text,  ((self.pos_x + (self.width - sub_text_width)  // 2), sub_text_y))
        