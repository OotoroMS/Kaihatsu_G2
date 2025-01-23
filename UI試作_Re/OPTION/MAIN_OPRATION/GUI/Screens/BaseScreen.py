# 画面生成・処理の管理クラス
# スクリーンはこのクラスを継承して作成する。
import pygame
from typing import  Tuple, Optional
# 部品
from MAIN_OPRATION.GUI.Parts.Button   import Button
from MAIN_OPRATION.GUI.Parts.Picture  import Picture

class BaseScreen:
    def __init__(self, screen : pygame.Surface) -> None:
        self.screen = screen
        self.setting_images()
        self.setting_buttons()
        
    # 画像の設定
    def setting_images(self):
        self.images : Picture = list()

    # ボタンの設定
    def setting_buttons(self):
        self.buttons : Button = list()
    
    # 描画
    def draw(self):
        self.draw_images()
        self.draw_buttons()
    
    # 画像を描画
    def draw_images(self):
        for image in self.images:
            if type(image) == Picture:
                image.draw()
    
    # ボタンを描画
    def draw_buttons(self):
        for button in self.buttons:
            if type(button) == Button:
                button.draw()
    
    # クリック判定
    def click_event(self):
        result = None
        normal = False
        for event in pygame.event.get():
            result, normal = self.clicked(event)
            if normal:
                return result, normal
        return result, normal
    
    # どのボタンの処理か判定して実行
    def clicked(self, event : pygame.event.Event) -> Tuple[Optional[str], bool]:
        result = None
        normal = False
        for button in self.buttons:
            if type(button) == Button:
                result, normal = button.is_clicked(event)
            if normal:
                return result, normal
        return result, normal