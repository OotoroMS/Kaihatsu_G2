import pygame
from typing import Tuple, Optional, List
# ベースクラス
from MAIN_OPRATION.GUI.Popups.BasePopup import BasePopup
# 定数
from MAIN_OPRATION.GUI.Constants.file_path         import *
from MAIN_OPRATION.GUI.Constants.popup_name  import *
from MAIN_OPRATION.GUI.Constants.color             import *
from MAIN_OPRATION.GUI.Constants.popup_text  import *
from MAIN_OPRATION.GUI.Constants.normal            import *
# 部品
from MAIN_OPRATION.GUI.Parts.Button         import Button
from MAIN_OPRATION.GUI.Parts.Picture        import Picture

class PassPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, text_index1 : str, text_index2 : str) -> None:
        super().__init__(screen)
        self.text_index = [text_index1, text_index2]
        self.setting_text()

        # テキストを生成
    def setting_text(self):
        self.view_texts: List[pygame.Surface] = []
        for text in self.text_index:
            self.view_texts.append(self.text_font.render(POPUP_TEXT[text], True, WHITE))

    # ボタンの設定
    def setting_buttons(self):
        button_width  = self.width  // 4
        button_height = self.height // 4
        button_x      = self.pos_x + (self.width // 2) - (button_width // 2)
        button_y      = self.height - (self.height // 4)
        self.buttons = [
            Button(self.screen, (button_x, button_y), (button_width, button_height), BACK_BOTTON_FILE_PATH, self.close_popup)
        ]
    
    # 描画処理
    def draw(self):
        super().draw()
        # 各行の高さを足す
        total_text_height = 0
        for text in self.view_texts:
            total_text_height += text.get_height()
        # 上からのマージン
        text_margin_top = 320
        # 全体の高さ
        total_height = total_text_height + text_margin_top

        # テキスト全体の開始位置(中央揃え)
        y = (self.height - total_height) //2 + self.pos_y

        # 各行の描画
        for text in self.view_texts:
            try:
                # x軸の位置(中央揃え)
                text_width = text.get_width()
                x = self.pos_x + (self.width - text_width) // 2
                # テキストの描画
                self.screen.blit(text, (x, y))
                y += text.get_height()
            except Exception as e:
                print(f"[Error] Failed to draw text: {e}")

    # ボタンのイベント処理
    def close_popup(self):
        return True, OK
    