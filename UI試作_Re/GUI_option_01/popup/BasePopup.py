#メインメニューの終了確認ポップアップ
import pygame
from typing               import Tuple, Optional
from parts.CaluclatePopup import *
from screen.BaseScreen    import BaseFrame
from parts.Button         import Button
from constant.FilePath    import *

GRAY = ((200,200,200))      #   カラーコード(灰色)
BLACK = ((255,255,255))     #   カラーコード(黒)
WHITE = ((0,0,0))           #   カラーコード(白)
BASEMSSEGE = "BASE POPUP"
BACKFRAME  = BUTTONFILEPATH + "back.png" # 戻るボタン

class BasePopup(BaseFrame):
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font, text : str):
        super().__init__(screen, font)
        self.text_font = pygame.font.Font(font, 100)
        self.rect = self.create_popup_rect()
        self.text = text
        self.view_text = self.text_font.render(self.text, True, WHITE)
        button_whidh = self.width // 4
        self.buttons = {
            Button(self.screen, self.pos_x + (self.width - button_whidh) // 2, self.height - (self.height // 4) , self.width // 4,self.height//4, BACKFRAME, self.back)      
        }

    def create_popup_rect(self) -> Optional[pygame.rect.Rect]:
        """
        popup画面の範囲を計算し、表示領域を生成するモジュール。
        """
        self.base_width, self.base_height = pygame.display.get_window_size()
        self.width, self.height = calculate_popup_size(self.base_width, self.base_height)
        self.pos_x, self.pos_y = caluclate_popup_position(self.base_width,self.base_height, self.width, self.height)
        if self.pos_x and self.pos_y:
            return pygame.rect.Rect(self.pos_x, self.pos_y, self.width, self.height)
        else:
            return None
    
    def update(self):
        move = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    move = button.is_clicked(event)
                    if move:
                        return move
        return move

    def draw(self):
        """
        画面更新処理。
        """
        if self.rect:
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)
            view_text_width = self.view_text.get_width()
            view_text_x = self.pos_x + (self.width - view_text_width) // 2
            self.screen.blit(self.view_text, ((view_text_x, self.height // 2)))
            for button in self.buttons:
                button.draw()
        else:
            print("失敗")              
    
    def back(self):
        return True