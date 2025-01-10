# パスワード入力ミス伝達用ポップアップ
import pygame
from typing import Tuple, Optional

from pygame.font import Font
# 部品
from GUI.parts.CaluclatePopup   import *
from GUI.parts.Button           import Button
from GUI.parts.Picture          import Picture
# 定数
from GUI.constants.popup_configs.pass_error_config  import *
from GUI.constants.file_path                        import *
from GUI.constants.color                            import *
# ベース
from GUI.popups.BasePopup   import BasePopup

class PassErrorPopup(BasePopup):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.main_text = self.text_font.render(MAIN_TEXT, True, WHITE)
        self.sub_text  = self.text_font.render(SUBTEXT,  True, WHITE)
        # 画像を読み込む
        image_x = self.pos_x + (self.width // 2) - (IMAGE_SIZE[0] // 2)
        image_y = self.pos_y + 25
        self.images.append(Picture(self.screen, (image_x, image_y), (IMAGE_SIZE[0], IMAGE_SIZE[1]), FAIL_IMAGE))

    def setting_buttons(self):
        button_width  = self.width  // 4
        button_height = self.height // 4
        button_x      = self.pos_x + (self.width // 2) - (button_width // 2)
        button_y      = self.height - (self.height // 4)
        self.buttons = [
            Button(self.screen, (button_x, button_y), (button_width, button_height), BACK_BOTTON_FILE_PATH, self.close_popup)
        ]

    def draw(self):
        super().draw()
        self.text_draw()

    def text_draw(self):
        main_text_width  = self.main_text.get_width()
        main_text_height = self.main_text.get_height()
        main_text_y      = self.pos_y + TEXT_DISTANSE

        sub_text_width = self.sub_text.get_width()
        sub_text_y     = main_text_height + main_text_y

        self.screen.blit(self.main_text, ((self.pos_x + (self.width - main_text_width) // 2), main_text_y))
        self.screen.blit(self.sub_text,  ((self.pos_x + (self.width - sub_text_width)  // 2), sub_text_y))
        
    # ボタンのイベント処理
    def close_popup(self):
        return True, True