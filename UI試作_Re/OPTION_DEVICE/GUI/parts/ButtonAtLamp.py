# ランプ付きのボタン
import sys
sys.path.append("../MAIN_DEVICE/GUI")
# デバック用はここまで
import pygame
from typing             import Tuple,Optional
from GUI.constant.color import *
from GUI.parts.Button   import *
from GUI.parts.Lamp     import Lamp

LAMP_SIZE       = [40, 40]
LAMP_X_DISTANSE = 40 + LAMP_SIZE[X]
LAMP_Y_DISTANSE = LAMP_SIZE[Y] // HALF

class ButtonAtLamp(Button):
    def __init__(self, screen: pygame.surface, coordinate: Tuple[int], size: Tuple[int], image_path: str, func) -> None:
        super().__init__(screen, coordinate, size, image_path, func)
        self.lamp_x = self.cordinate[X] + self.size[WIDTH] - LAMP_X_DISTANSE
        self.lamp_y = self.cordinate[Y] + (self.size[HEIGHT] // HALF) - LAMP_Y_DISTANSE
        self.lamp = Lamp(self.screen, self.lamp_x, self.lamp_y, LAMP_SIZE[WIDTH], LAMP_SIZE[HEIGHT], YELLOW)
    
    # 描画処理
    def draw(self):
        self.hover_button()
        self.screen.blit(self.image, self.rect)
        self.lamp.draw()

    # 拡大判定処理
    def hover_button(self):
        if self.flag_hover:
            pos     = pygame.mouse.get_pos()
            hovered = self.rect.collidepoint(pos)
            if hovered:
                self.expansion_button()
                self.expansion_lamp()
            else:
                self.default_button()
                self.default_lamp()
        else:
            self.default_button()
            self.default_lamp()

    # ランプ拡大処理
    def expansion_lamp(self):
        width  = self.size[WIDTH]  * SIZE_SCALE
        height = self.size[HEIGHT] * SIZE_SCALE // HALF
        rect_xy = self.rect.topleft
        expansion_lamp_x = (width  + rect_xy[X]) - LAMP_X_DISTANSE * SIZE_SCALE
        expansion_lamp_y = (height + rect_xy[Y]) - LAMP_Y_DISTANSE * SIZE_SCALE
        expansion_lamp_width = LAMP_SIZE[WIDTH]   * SIZE_SCALE
        expansion_lamp_height = LAMP_SIZE[HEIGHT] * SIZE_SCALE
        self.lamp.update_rect(expansion_lamp_x, expansion_lamp_y, expansion_lamp_width, expansion_lamp_height)

    # ランプサイズ初期化処理
    def default_lamp(self):
        self.lamp.update_rect(self.lamp_x, self.lamp_y, LAMP_SIZE[WIDTH], LAMP_SIZE[HEIGHT])
    
    # ランプの色を更新
    def update_lamp_color(self, color):
        self.lamp.update_color(color)
