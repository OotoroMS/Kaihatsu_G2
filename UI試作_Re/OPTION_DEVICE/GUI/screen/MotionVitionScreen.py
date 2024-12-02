import pygame
# 定数
from GUI.constant.judge_result                  import *
from GUI.constant.screen.motion_vition_constant import * 
from GUI.constant.screen.screen_name            import *
from GUI.constant.popup.popup_name              import *
# 部品
from GUI.parts.Button   import *
from GUI.parts.Picture  import *
# 画面クラス
from GUI.screen.BaseScreen  import BaseScreen

class MotionVitionScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
    
    # ボタンの設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_BACK_STATUS,     func=self.back),
            Button(self.screen, **BUTTON_SOLENOID_STATUS, func=self.solenoid),
            Button(self.screen, **BUTTON_STAPING_STATUS,  func=self.staping)
        ]
    
    def setting_images(self):
        self.images = [
            Picture(self.screen, **TITLE_MOTION_VITION_STATUS)
        ]

    def back(slef):
        return MOTION, OK
    
    def solenoid(self):
        return "key", OK
    
    def staping(self):
        return "key", OK