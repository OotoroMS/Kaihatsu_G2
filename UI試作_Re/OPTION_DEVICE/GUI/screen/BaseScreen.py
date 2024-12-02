# 画面生成・処理の管理クラス
# スクリーンはこのクラスを継承して作成する。
# 継承先で"setting_immages"と"setting_buttons"の処理を書き換えてください。
# 継承先で"self.images"と"self.buttons"以外の画像やボタンが増えた場合は
# 画像のみなら"draw"を、ボタンの場合は"draw"と"clicked"を書き換えてください。
import pygame
from typing import  Tuple, Optional
# 部品
from GUI.parts.Button   import Button
from GUI.parts.Picture  import Picture
# 定数
from GUI.constant.judge_result import *

class BaseScreen:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen = screen
        self.setting_images()
        self.setting_buttons()
        
    # 画像の設定
    def setting_images(self):
        self.images = []

    # ボタンの設定
    def setting_buttons(self):
        self.buttons = []
    
    # 描画処理
    def draw(self):
        self.draw_images()
        self.draw_buttons()
        
    # ボタンを描画
    def draw_buttons(self):
        for button in self.buttons:
            if type(button) == Button:
                button.draw()
    
    # 画像を描画
    def draw_images(self):
        for image in self.images:
            if type(image) == Picture:
                image.draw()

    # クリック判定時の処理
    def click_event(self):
        result = None
        normal = FAILURE
        for event in pygame.event.get():
            result, normal = self.clicked(event)
            if normal:
                return result, normal
        return result, normal
    
    # どのボタンの処理か判定して実行
    def clicked(self, event : pygame.event.Event) -> Tuple[Optional[str], bool]:
        result = None
        normal = FAILURE
        for button in self.buttons:
            if type(button) == Button:
                result, normal = button.is_clicked(event)
            if normal:
                return result, normal
        return result, normal
