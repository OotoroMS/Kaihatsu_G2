
import pygame
import os
import Graph
from BaseFrame import BaseFrame
from Button import Button

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
PATH = "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\graph.png"

class GraphFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.create_flg = True
        self.text_title = self.font_title.render("寸法検査ログ", True, BLACK)
        self.buttons = {
            Button(self.screen, 1570, 930, 330, 120, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\return.png", self.move_data)
        }
    
    #   画面描画処理
    def draw(self):
        self.screen.blit(self.text_title,(200,50))
        self.draw_graph()
        self.screen.blit(self.graph, (100,120))
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