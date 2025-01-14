#寸法検査ログ
import pygame
import os
import graph.Graph as Graph
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from filepath import *

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
PATH = IMAGEFILEPATH + "graph.png"

class GraphFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.create_flg = True
        self.buttons = {
            Button(self.screen, 0, 960, 330, 120, IMAGEFILEPATH + "button\\back.png", self.move_data)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, IMAGEFILEPATH + "title\\pic18.png")
        }
    
    #   画面描画処理
    def draw(self):
        for image in self.images:
            image.draw()
        self.draw_graph()
        self.screen.blit(self.graph, (270,190))
        for button in self.buttons:
            button.draw()
    
    #   グラフ描画・更新処理
    def draw_graph(self):
        if self.create_flg:
            self.create_flg = False
            Graph.graph()
            if os.path.exists(PATH):
                self.graph = pygame.image.load(PATH)
            self.graph_image = pygame.transform.scale(self.graph,(1100,900))

    #   データ一覧画面に遷移
    def move_data(self):
        self.create_flg = True
        return "data"