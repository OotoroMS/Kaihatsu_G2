import pygame
from typing import Tuple, Optional
# ベースクラス
from MEINTENANCE.GUI.popups.BasePopup import BasePopup
# 定数(コマンド)
from MEINTENANCE.CONSTANTS.command_type import *
# 定数(GUI)
from MEINTENANCE.GUI.constants.popup_configs.Back_config    import *
from MEINTENANCE.GUI.constants.file_path                    import *
from MEINTENANCE.GUI.constants.popup_name                   import *
from MEINTENANCE.GUI.constants.screen_name                  import *
from MEINTENANCE.GUI.constants.color                        import *
from MEINTENANCE.GUI.constants.popup_text                   import *
# 部品
from MEINTENANCE.GUI.parts.Button         import Button
from MEINTENANCE.GUI.parts.Picture        import Picture

class BackPopup(BasePopup):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.setting_text()

    def setting_text(self):
        self.view_text = self.text_font.render(POPUP_TEXT[BACK_POPUP], True, WHITE)
    
    def setting_buttons(self):
        button_width  = self.width  // 4
        button_height = self.height // 4
        button_no_x  = self.pos_x + (self.width // 2) + (button_width // 2)
        button_yes_x   = self.pos_x + (button_width // 2)
        button_y      = self.height - (self.height // 4)
        self.buttons = [
            Button(self.screen, (button_yes_x, button_y), (button_width, button_height), BUTTON_YES_FILE_PATH,  self.yes),
            Button(self.screen, (button_no_x, button_y),  (button_width, button_height), BUTTON_NO_FILE_PATH, self.no)
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
        return END, True   
    
    def no(self):
        return None, True