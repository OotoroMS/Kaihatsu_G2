import pygame
# 定数
from MEINTENANCE.GUI.constants.button_result                import *
from MEINTENANCE.CONSTANTS.command                      import *
from MEINTENANCE.GUI.constants.screen_name                  import *
from MEINTENANCE.GUI.constants.screen_configs.vision_config import *
# 部品
from MEINTENANCE.GUI.parts.Button   import Button
from MEINTENANCE.GUI.parts.Picture  import Picture
import MEINTENANCE.GUI.parts.ButtonAtLamp as ButtonAtLamp
# べース
from MEINTENANCE.GUI.screens.BaseScreen  import BaseScreen

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

        self.lamp_buttons = [
            ButtonAtLamp.ButtonAtLamp(self.screen, **BUTTON_LIGHT_STATUS, func=self.light_on),
            ButtonAtLamp.ButtonAtLamp(self.screen, **BUTTON_LIGHT_STATUS, func=self.light_off)
        ]
        self.lamp_buttons[ON].update_lamp_color(GREEN)
        self.lamp_buttons[OFF].update_lamp_color(GRAY)
        self.lamp_mode = OFF

    def draw(self):
        super().draw()
        self.lamp_buttons[self.lamp_mode].draw()

    def click_event(self):
        result = None
        normal = False
        for event in pygame.event.get():
            result, normal = self.clicked(event)
            if normal:
                # print("VisionScreen.py class:VisionScreen def:cxlick_event text: return")
                return result, normal
            # ランプ付きボタンのクリック判定
            result, normal = self.lamp_buttons[self.lamp_mode].is_clicked(event)
            # print("VisionScreen.py class:VisionScreen def:cxlick_event text: self.lamp_mode = ", self.lamp_mode)
            if normal:
                if self.lamp_mode == OFF:
                    self.lamp_mode = ON
                else:
                    self.lamp_mode = OFF
                # return result, normal
        return result, normal

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
    
    def light_on(self):
        # self.lamp_mode = ON
        print("VisionScreen.py class:VisionScreen def:light_on text: return")
        return LIGHT_ON, PRESS
    
    def light_off(self):
        print("VisionScreen.py class:VisionScreen def:light_off text: return")
        # self.lamp_mode = OFF
        return LIGHT_OFF, PRESS