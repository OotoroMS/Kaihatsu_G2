import pygame
from typing               import Tuple, Optional

from pygame.font import Font
from parts.CaluclatePopup import *
from popup.BasePopup      import BasePopup
from parts.Button         import Button
from constant.FilePath    import *

GRAY = ((200,200,200))      #   カラーコード(灰色)
BLACK = ((255,255,255))     #   カラーコード(黒)
WHITE = ((0,0,0))           #   カラーコード(白)

ENDPOPUP  = "終了しますか？"
BACKFRAME = BUTTONFILEPATH + "back.png"
ENDFRAME  = BUTTONFILEPATH + "pic04.png"
BASEPASH  = EXPTXTFILEPATH + "pic75.png"

class EndPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, font: Font):
        super().__init__(screen, font, "")
        self.text = ENDPOPUP
        self.veiw_text = self.text_font.render(self.text, True, WHITE)
        self.buttons = [
            Button(self.screen, (self.width // 2) - (self.width // 4), self.height - (self.height // 4) , self.width // 4,self.height//4, ENDFRAME,  self.YES),     
            Button(self.screen, (self.width // 2) + (self.width // 8), self.height - (self.height // 4) , self.width // 4,self.height//4, BACKFRAME, self.NO)
        ]
    
    def update(self):
        reaction = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    reaction = button.is_clicked(event)
                    if reaction:
                        return reaction
        return reaction

    def draw(self):
        """
        画面更新処理。
        """
        if self.rect:
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)
            text_width = self.veiw_text.get_width()
            self.screen.blit(self.veiw_text, (((self.pos_x + (self.width  - text_width)// 2), self.height // 2)))
            for button in self.buttons:
                button.draw()
        else:
            print("失敗")              
    
    def YES(self):
        return "yes"
    
    def NO(self):
        return "no"