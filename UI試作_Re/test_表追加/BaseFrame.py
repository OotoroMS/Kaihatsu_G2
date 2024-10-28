import pygame
from pygame.locals import *

class BaseFrame():
    def __init__(self, screen):
        self.screen = screen
    
    #   イベント処理を記述
    def update(self):
        pass

    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        pass
