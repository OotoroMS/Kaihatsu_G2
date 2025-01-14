# ボタンの描画・押下処理を行うクラス
#　デバック用
import sys
sys.path.append("../MAIN_DEVICE/GUI")
# デバック用はここまで
import pygame
from typing             import Tuple,Optional
from GUI.constant.color import *

HOVER_ON        = True
HOVER_OFF       = False
SIZE_SCALE      = 1.1
CORDINATE_SCALE = SIZE_SCALE - 1
HALF            = 2
X               = 0
Y               = 1
WIDTH          = 0
HEIGHT          = 1

class Button:
    # screen:pygameのスクリーン coordinate:X,Y座標 size:ボタンの縦幅と横幅
    # image_path:ボタンの画像ファイルパス func:紐づける処理
    def __init__(self, screen : pygame.surface, coordinate : Tuple[int, int], size : Tuple[int, int], image_path : str, func) -> None:
        self.screen            = screen
        self.cordinate         = coordinate
        self.size              = size
        self.base_image        = pygame.image.load(image_path)
        self.base_rect         = self.base_image.get_rect()
        self.base_rect.topleft = self.cordinate
        self.func              = func
        self.flag_hover        = HOVER_ON
        self.presse            = False

        self.default_button()

    # 描画処理
    def draw(self):
        self.hover_button()
        self.screen.blit(self.image, self.rect)

    # 拡大判定処理
    def hover_button(self):
        if self.flag_hover:
            pos     = pygame.mouse.get_pos()
            hovered = self.rect.collidepoint(pos)
            if hovered:
                self.expansion_button()
            else:
                self.default_button()
        else:
            self.default_button()

    # ボタンを拡大する
    def expansion_button(self):
        # 拡大処理
        x      = self.sum_size(self.cordinate[X], self.size[WIDTH])
        y      = self.sum_size(self.cordinate[Y], self.size[HEIGHT])
        width  = self.size[WIDTH] * SIZE_SCALE
        height = self.size[HEIGHT] * SIZE_SCALE

        self.image = pygame.transform.scale(self.base_image, (width, height))
        rect         = self.image.get_rect()
        rect.topleft = (x, y)
        self.rect    = rect

    # 座標計算
    def sum_size(self,coordiante, size):
        # 大きくしたときの座標
        hover_coordiante = coordiante - (size * CORDINATE_SCALE) // HALF
        return hover_coordiante

    # ボタンのサイズを通常時に戻す
    def default_button(self):
        self.image = pygame.transform.scale(self.base_image, self.size)
        self.base_rect = self.image.get_rect()
        self.base_rect.topleft = self.cordinate
        self.rect  = self.base_rect
    
    # 拡大機能を切る
    def off_hover_flag(self):
        self.flag_hover = HOVER_OFF

    # 押下処理
    def is_clicked(self, event):
        result = None
        normal = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                result, normal = self.func()        
        return result, normal
    
    # 必ず動作前にpygame.event.getを実行する
    def is_pressed(self, event):
        result = None
        normal = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.cnt = 0
                self.presse = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                print("end")
                self.presse = False
        if self.presse:
            print("push :", self.cnt)
            self.cnt += 1
            result, normal = self.func()  
            return result, normal
        return  result, normal
    