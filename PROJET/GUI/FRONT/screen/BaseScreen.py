# GUI/FRONT/screen/BaseScreen.py

# デバック用
import sys
import os
sys.path.append(os.getcwd())

import pygame
from queue import Queue
from typing import Tuple, Optional

# 自作プログラムをimport
from GUI.FRONT.parts.Button import Button
# 定数ファイル
from GUI.FRONT.constant.button import BtnBase
from GUI.FRONT.constant.background import BackBase

class BaseScreen:
    def __init__(self, screen: pygame.Surface, to_back: Queue):
        self.screen: pygame.Surface = screen    # 部品を置く画面
        self.to_back: Queue = to_back
        self.setting_images()   # 画像配置
        self.setting_buttons()  # ボタン配置  
        self.background = BackBase.Base
    
    def setting_images(self):
        # 配置する画像達
        self.images = [
            None
        ]
    
    def setting_buttons(self):
        # 配置するボタン達
        self.buttons: list[Button] = [
            None
        ]
    
    def images_draw(self):
        for image in self.images:
            if image:
                image.draw()

    def buttons_draw(self):
        for button in self.buttons:
            if button:
                # ボタンの描画処理
                button.draw()
    
    def draw(self):
        # 背景の描画
        self.background.scale_to_window(self.screen)
        self.background.draw(self.screen)
        # 画像とボタンの描画処理
        self.images_draw()
        self.buttons_draw()
    
    def func(self):
        # ボタンに紐付ける関数(例)
        print("ボタンが押されました")        
    
    def process_back_response(self, response):
        # バックからの応答を画面で処理
        print(f"BaseScreenでバックからのレスポンスを処理: {response}")        
        # ここで表示画面を変更するのは無理があると思うのだけれど
    
    def handle_event(self, event: pygame.event.Event):
        for button in self.buttons:
            button.check_click(event)