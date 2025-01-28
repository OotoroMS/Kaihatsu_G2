import pygame
from typing import Tuple, Optional
# ベースクラス
from MAIN_OPRATION.GUI.Popups.BasePopup import BasePopup
# 定数
from MAIN_OPRATION.GUI.Constants.file_path  import *
from MAIN_OPRATION.GUI.Constants.color      import *
from MAIN_OPRATION.GUI.Constants.normal     import *
from MAIN_OPRATION.GUI.Constants.popup_text import *
from MAIN_OPRATION.GUI.Constants.popup_name import *

# 部品
from MAIN_OPRATION.GUI.Parts.Button         import Button
from MAIN_OPRATION.GUI.Parts.Picture        import Picture

class EndPopup(BasePopup):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.setting_text()

    # テキストの設定
    def setting_text(self):
        self.text = self.text_font.render(POPUP_TEXT[END_POPUP], True, WHITE)
    
    def setting_buttons(self):
        button_width  = self.width  // 4
        button_height = self.height // 4
        button_yes_x  = self.pos_x + (self.width // 2) + (button_width // 2)
        button_no_x   = self.pos_x + (button_width // 2)
        button_y      = self.height - (self.height // 4)
        self.buttons = [
            Button(self.screen, (button_yes_x, button_y), (button_width, button_height), BACK_BOTTON_FILE_PATH, self.no),
            Button(self.screen, (button_no_x, button_y), (button_width, button_height), END_BOTTON_FILE_PATH, self.yes)
        ]
    
    # 描画処理
    def draw(self):
        super().draw()
        width  = self.text.get_width()
        height = self.text.get_height()
        x = self.pos_x + (self.width  // 2) - (width // 2)
        y = (self.height // 2) - (height // 2)
        self.screen.blit(self.text, (x, y))

    # ボタンのイベント処理
    def yes(self):
        return True, OK
    
    def no(self):
        return False, OK
