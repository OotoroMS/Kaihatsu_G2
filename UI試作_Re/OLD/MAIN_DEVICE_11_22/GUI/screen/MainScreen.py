#メインメニュー
import pygame
import sys
import os
sys.path.append(os.getcwd())
from typing               import Tuple,Optional
# 定数
from GUI.constant.file_path   import *
from GUI.constant.screen_name import *
from GUI.constant.popup_name  import *
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture
from GUI.screen.BaseScreen    import BaseScreen

MAIN_TETLE_STATUS    = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_main.png"
}
EXPTXT_DATA_STATUS   = {
    "coordinate" : (175, 600),
    "size"       : (650, 350),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_data.png"
}
EXPTXT_MOTION_STATUS = {
    "coordinate" : (1025,600),
    "size"       : (650, 350),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_motion.png"
}
BUTTON_DATA_STATUS   = {
    "coordinate" : (150, 300),
    "size"       : (700, 350),
    "image_path" : BUTTON_FILE_PATH + "button_data.png"
}
BUTTON_MOTION_STATUS = {
    "coordinate" : (1000,300),
    "size"       : (700, 350),
    "image_path" : BUTTON_FILE_PATH + "button_motion.png"
}
BUTTON_END_STATUS    = {
    "coordinate" : (0,   960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_end.png"
}

class MainScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
    
    # 表示画像設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **MAIN_TETLE_STATUS),
            Picture(self.screen, **EXPTXT_DATA_STATUS),
            Picture(self.screen, **EXPTXT_MOTION_STATUS)
        ]
    
    # 表示ボタン設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_DATA_STATUS,   func=self.move_data),
            Button(self.screen, **BUTTON_MOTION_STATUS, func=self.move_motion),
            Button(self.screen, **BUTTON_END_STATUS,    func=self.end_app)
        ]
    
    # データ一覧画面に遷移
    def move_data(self):
        return DATA, OK
    
    # 動作確認画面に遷移
    def move_motion(self):
        return PASS, OK
    
    # 終了処理
    def end_app(self):
        return END, OK