# 画面生成・処理の管理クラス
# スクリーンはこのクラスを継承して作成する。
# 継承先で"setting_immages"と"setting_buttons"の処理を書き換えてください。
# 継承先で"self.images"と"self.buttons"以外の画像やボタンが増えた場合は
# 画像のみなら"draw"を、ボタンの場合は"draw"と"clicked"を書き換えてください。
import pygame
import sys
sys.path.append("../MAIN_DEVICE/GUI")
from typing               import Tuple,Optional
# 定数
from constant.file_path   import *
from constant.screen_name import *
from parts.Button         import Button
from parts.Picture        import Picture

BASE_TAITLE_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (200, 200),
    "image_path" : TITLE_FILE_PATH + "title_main.png"
}
BACK_BOTTON_STATUS = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}

class BaseScreen:
    def __init__(self, screen : pygame.Surface):
        self.screen = screen
        self.setting_images()
        self.setting_buttons()
    
    # 表示画像設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **BASE_TAITLE_STATUS)
        ]
    
    # 表示ボタン設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS, func=self.base_button_func)
        ]
    
    # 描画処理
    def draw(self):
        for image  in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()

    # 押下判定
    def click_event(self):
        result = None
        normal = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                result, normal = self.clicked(event)
                return result, normal
            if event.type == pygame.MOUSEBUTTONUP:
                result, normal = self.clicked(event)
                return result, normal
        return result, NG
    
    # クリック(タップ)時の処理
    def clicked(self, event):
        result = ""
        normal = False
        # ボタンに位置でクリック(タップ)されていたら紐づけられた処理を行う
        for button in self.buttons:
            result,normal = button.is_clicked(event)
            if normal:
                return result, normal
        return result, normal

    # 押下処理(デバック用)
    def base_button_func(self):
        print("BaseScreen以外で表示された場合はボタンの設定を確認してください")
        return BASE, OK
    