#メインメニューの終了確認ポップアップ
import pygame
from typing import Tuple, Optional
from CaluclatePopup import *
from BaseFrame import BaseFrame
from Button import Button

GRAY = ((200,200,200))      #   カラーコード(灰色)
BLACK = ((255,255,255))     #   カラーコード(黒)
WHITE = ((0,0,0))           #   カラーコード(白)
BASEMSSEGE = "BASE POPUP"
BACKFRAME = "GUI_option_test\\image\\button\\back.png"#戻るボタン

class BasePopup(BaseFrame):
    def __init__(self, screen : pygame.Surface, font : pygame.font.Font, text : str):
        super().__init__(screen, font)
        self.text_font = pygame.font.Font(font, 100)
        self.rect = self.create_popup_rect()
        self.text = text
        self.text_message = self.text_font.render(self.text, True, WHITE)
        self.buttons = {
            Button(self.screen, (self.width // 2) - (self.width // 8), self.height - (self.height // 4) , self.width // 4,self.height//4, BACKFRAME, self.back)      
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
        move = True
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    move = button.is_clicked(event)
                    if move == False:
                        return move
        return True

    def draw(self):
        """
        画面更新処理。
        """
        if self.rect:
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)
            self.screen.blit(self.text_message, (((self.width // 4), self.height // 2)))
            for button in self.buttons:
                button.draw()
        else:
            print("失敗")              
    
    def back(self):
        return False