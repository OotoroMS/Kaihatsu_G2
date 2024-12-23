import pygame
# 定数
from GUI.constants.button_result                import *
from CONSTANTS.command                      import *
from GUI.constants.screen_name                  import *
from GUI.constants.screen_configs.vision_config import *
# 部品
from GUI.parts.Button   import Button
from GUI.parts.Picture  import Picture
# べース
from GUI.screens.BaseScreen  import BaseScreen

class VitisonScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
    
    # ボタンの設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_BACK_STATUS,     func=self.back),
            Button(self.screen, **BUTTON_SOLENOID_STATUS, func=self.solenoid),
            Button(self.screen, **BUTTON_STAPING_STATUS,  func=self.staping)
        ]
    
    # 画像の設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **TITLE_MOTION_VITION_STATUS)
        ]
    
    def back(self):
        return MAIN, PRESS

    def solenoid(self):
        return SOLENOID, PRESS
    
    def staping(self):
        return STEPING, PRESS