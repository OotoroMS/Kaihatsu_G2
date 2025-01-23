import pygame
from typing import Tuple, Optional
# 定数
from MEINTENANCE.GUI.constants.popup_configs.Operation_config   import *
from MEINTENANCE.GUI.constants.popup_name                       import *
from MEINTENANCE.GUI.constants.file_path                        import *
from MEINTENANCE.GUI.constants.color                            import *

# 基準
from MEINTENANCE.GUI.popups.BasePopup   import BasePopup

FONT_SIZE = 100

class OperationPopup(BasePopup):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.setting_text()
    
    def setting_text(self):
        self.oprating_text = self.text_font.render(OPERATING_TEXT, True, WHITE)
        self.waiting_text  = self.text_font.render(WAITING_TEXT,   True, WHITE)
    
    def draw(self):
        super().draw()
        # 1行目
        width   = self.oprating_text.get_width()
        height  = self.oprating_text.get_height()
        # 座標を計算
        x = self.pos_x + (self.width - width) // 2
        y = (self.height - height*2) // 2 + self.pos_y
        # 1行目を描画
        self.screen.blit(self.oprating_text, (x, y))
        # 2行目
        width = self.waiting_text.get_width()
        # 座標を計算
        x = self.pos_x + (self.width - width) // 2
        y += self.waiting_text.get_height()
        self.screen.blit(self.waiting_text,  (x, y))