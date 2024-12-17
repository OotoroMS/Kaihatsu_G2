# GUI/FRONT/popup/BasePopup.py

# デバック用
import sys
import os
sys.path.append(os.getcwd())

import pygame
from queue import Queue
from typing import Tuple, Optional

# 自作プログラムをimport
from GUI.FRONT.parts.Button import Button
from GUI.FRONT.parts.Text   import Text
from GUI.FRONT.constant.file_path import FONT
from GUI.FRONT.constant.color     import GRAY, BLACK

class BasePopup:    
    def __init__(self, screen: pygame.Surface, to_back: Queue):
        self.screen: pygame.Surface = screen    # 部品を置く画面
        self.to_back: Queue = to_back
        self.text_font = pygame.font.Font(FONT, 100)
        # ポップアップの作成
        self.rect = self.popup()
        # 各部品の配置
        self.setting_images()
        self.setting_buttons()
        self.setting_texts()
    
    def setting_images(self):
        self.images = [
            None
        ]
    
    def setting_texts(self):
        self.texts: list[Text] = [
            None
        ]
    
    def setting_buttons(self):
        self.buttons: list[Button] = [
            None
        ]
    
    def images_draw(self):
        for image in self.images:
            if image:
                # 画像の描画処理
                image.draw()

    def buttons_draw(self):
        for button in self.buttons:
            if button:
                # ボタンの描画処理
                button.draw()
    
    def texts_draw(self):
        for text in self.texts:
            if text:
                # テキストの描画処理
                text.draw()
    
    def draw(self):
        if self.rect:
            # 背景の描画
            pygame.draw.rect(self.screen, GRAY, self.rect)
            pygame.draw.rect(self.screen, BLACK, self.rect, 2)
            self.images_draw()
            self.buttons_draw()
            self.texts_draw()

    
    def popup(self):
        window_size = pygame.display.get_window_size()  # 画面サイズ取得
        # ポップアップのサイズ取得
        popup_width = window_size[0] - 200
        popup_height = window_size[1] - 200
        # ポップアップの座標取得
        popup_x     = (window_size[0] - popup_width) // 2
        popup_y     = (window_size[1] - popup_height) // 2
        if popup_x and popup_y:
            rect = pygame.rect.Rect(popup_x, popup_y, popup_width, popup_height)
            return rect
        else:
            return None
    
    def popup_update(self, text: str):
        for view_text in self.texts:
            if view_text:
                view_text.update(text)

    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.check_click(event)    