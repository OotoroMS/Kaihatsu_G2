import pygame
from GUI.constant.color import *
from typing         import Tuple,Optional
# from MAIN_DEVICE_11_22.GUI.constant.color import *
# 画像クラス
class Picture:
    # screen:pygameのスクリーン coordinate:X,Y座標 size:縦幅と横幅
    # image_path:画像ファイルパス
    def __init__(self, screen : pygame.surface, coordinate : Tuple[int, int], size : Tuple[int, int], image_path : str):
        self.screen         = screen
        self.base_image     = pygame.image.load(image_path)
        self.image          = pygame.transform.scale(self.base_image, size)
        self.rect           = self.image.get_rect()
        self.rect.topleft   = coordinate
    
    # 画像描画処理
    def draw(self):
        self.screen.blit(self.image, self.rect) # 画像を描画