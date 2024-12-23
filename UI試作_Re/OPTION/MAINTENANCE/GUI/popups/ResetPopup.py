import pygame
from typing import Tuple, Optional
# ベースクラス
from GUI.popups.BasePopup import BasePopup
# 定数(コマンド)
from CONSTANTS.command_type import *
# 定数
from GUI.constants.popup_configs.Reset_config   import *
from GUI.constants.popup_name                   import *
from GUI.constants.popup_text                   import *
from GUI.constants.file_path                    import *
from GUI.constants.color                        import *
# 部品
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture

class ResetPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, text_index : str) -> None:
        super().__init__(screen)
        self.setting_text(text_index)

    # テキストを生成
    def setting_text(self, text_index):
        if text_index in POPUP_TEXT.keys():
            # 表示用テキストを生成
            self.view_text = self.text_font.render(POPUP_TEXT[text_index], True, WHITE)

    # ボタンの設定
    def setting_buttons(self):
        button_width  = self.width  // 4
        button_height = self.height // 4
        button_yes_x  = self.pos_x + (self.width // 2) + (button_width // 2)
        button_no_x   = self.pos_x + (button_width // 2)
        button_y      = self.height - (self.height // 4)
        self.buttons = [
            Button(self.screen, (button_yes_x, button_y), (button_width, button_height), BUTTON_FILE_PATH + "button_no.png",  self.no),
            Button(self.screen, (button_no_x, button_y),  (button_width, button_height), BUTTON_FILE_PATH + "button_yes.png", self.yes)
        ]

    # 描画処理
    def draw(self):
        super().draw()
        width  = self.view_text.get_width()
        height = self.view_text.get_height()
        x = self.pos_x + (self.width  // 2) - (width // 2)
        y = (self.height // 2) - (height // 2)
        self.screen.blit(self.view_text, (x, y))

    # ボタンのイベント処理
    def yes(self):
        return DB_RESET, True   
    
    def no(self):
        return None, True