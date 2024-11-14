# 原点復帰ポップアップ
import pygame
from typing                 import Tuple, Optional

from pygame.font import Font

from popup.CaluclatePopup   import *
from popup.BasePopup        import BasePopup
from parts.Picture          import Picture
from filepath               import *

GRAY = ((200,200,200))      #   カラーコード(灰色)
BLACK = ((255,255,255))     #   カラーコード(黒)
WHITE = ((0,0,0))           #   カラーコード(白)

BACKFRAME  = IMAGEFILEPATH + "button\\back.png"
TOPMESSAGE     = "原点復帰を行います"

class OrigenPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, font: Font):
        super().__init__(screen, font, "")
        self.toptext = TOPMESSAGE
        self.toptext_image = self.text_font.render(self.toptext, True, WHITE)
    
    def draw(self):
        """
        画面更新処理。
        """
        if self.rect:
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)

            toptext_width = self.toptext_image.get_width()
            toptext_x     = self.pos_x + (self.width  - toptext_width) // 2
            toptext_y     = self.toptext_image.get_height() + self.pos_y
            
            self.screen.blit(self.toptext_image, (toptext_x, toptext_y))
            for button in self.buttons:
                button.draw()