import pygame
from typing import Tuple, Optional, List
# ベースクラス
from GUI.popup.BasePopup import BasePopup
# 共通の定数
from GUI.constant.file_path     import *
from GUI.constant.popup_name    import *
from GUI.constant.color         import *
from GUI.constant.normal        import *
# 個別の定数
from GUI.constant.popup.worning_constant    import *
# 部品
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture

class WarningPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, view_popup : str) -> None:
        self.view_popup = view_popup
        print(view_popup)
        super().__init__(screen)
        self.setting_texts()
    
    # テキストの設定
    def setting_texts(self):
        if self.view_popup == ACTIVE_PASS:
            print("NG")
            self.view_texts : List[pygame.Surface] = [
                self.text_font.render(POPUP_STOP_MESSAGE_01, True, WHITE),
                self.text_font.render(POPUP_STOP_MESSAGE_02, True, WHITE),
                self.text_font.render(POPUP_STOP_MESSAGE_03, True, WHITE)
            ]
        if self.view_popup == ORIGIN:
            print("OK")
            self.view_texts : List[pygame.Surface] = [
                self.text_font.render(POPUP_ORIGIN_MESSAGE_01, True, WHITE),
                self.text_font.render(POPUP_ORIGIN_MESSAGE_02, True, WHITE),
                self.text_font.render(POPUP_ORIGIN_MESSAGE_03, True, WHITE)
            ]

    def setting_images(self):
        # 大きさ
        image_width  = self.width // 7
        image_height = image_width
        # 座標
        if self.view_popup == ACTIVE_PASS:
            image_x =  self.pos_x + IMAGE_X_DISTANCE
        else:
            image_x =  self.pos_x + IMAGE_X_DISTANCE + ORIGIN_DISTANCE
        image_y = (self.pos_y + self.height) // 2 - image_height

        self.images = [
            Picture(self.screen, (image_x, image_y), (image_width, image_height), IMAGE_WARNING_PATH)
        ]
    
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
        text_margin_top = 300
        # 全体の高さ
        total_height = total_text_height + text_margin_top

        # テキスト全体の開始位置(中央揃え)
        y = (self.height - total_height) // 2 + self.pos_y

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