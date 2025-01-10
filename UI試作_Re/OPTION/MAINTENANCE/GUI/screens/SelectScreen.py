import pygame
# 定数
from GUI.constants.screen_configs.main_config   import *
from GUI.constants.screen_name                  import *
from GUI.constants.popup_name                   import *
# ベーススクリーン
from GUI.screens.BaseScreen import BaseScreen
# 部品
from GUI.parts.Button   import Button
from GUI.parts.Picture  import Picture

class SelectScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
    
    def setting_images(self):
        self.images = [
            Picture(self.screen, **TITLE_MAIN_CONFIG),
            Picture(self.screen, **EXP_TARGET_CONFIG)
        ]

    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_BACK_CONFIG,        func=self.back),
            Button(self.screen, **BUTTON_MOVING_CONFIG,      func=self.move),
            Button(self.screen, **BUTTON_VISION_CONFIG,      func=self.vision),
            Button(self.screen, **BUTTON_CHANGE_PASS_CONFIG, func=self.change),
            Button(self.screen, **BUTTON_RESET_CONFIG,       func=self.db_reset)
        ]
    
    def draw(self):
        self.draw_images()
        self.draw_lines()
        self.draw_buttons()
    
    def draw_lines(self):
        pygame.draw.line(self.screen, **LINE_RED_CONFIG)
        pygame.draw.line(self.screen, **LINE_BLUE_CONFIG)
    
    def back(self):
        return BACK_POPUP, True
    
    def vision(self):
        return VISION, True
    
    def move(self):
        return MOVE, True
    
    def change(self):
        return CHANGE, True
    
    def db_reset(self):
        return DB_RESET_POPUP, True