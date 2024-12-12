# GUI/FRONT/parts/Button.py

import pygame
from typing import Tuple
# 自作プログラムをimport

class Button:
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], 
                 size: Tuple[int, int], path: str, func):
        self.screen: pygame.Surface = screen    # ボタンを置く画面
        pos     # ボタンの座標
        size    # ボタンのサイズ
        path    # ボタンに表示する画像
        self.func = func    # ボタンに紐づける関数
        # ここでボタンの作成
        self.default_button(pos, size, path)
    
    def default_button(self, pos: tuple[int, int],
                       size: Tuple[int, int], path: str):
        self.img = pygame.image.load(path)
        self.img = pygame.transform.scale(self.img, size)
        self.img_rect = self.img.get_rect()
        self.img_rect.topleft = pos
    
    # ボタン描画
    def draw(self):
        self.screen.blit(self.img, self.img_rect)
    
    def check_click(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.img_rect.collidepoint(event.pos):
                self.func()
