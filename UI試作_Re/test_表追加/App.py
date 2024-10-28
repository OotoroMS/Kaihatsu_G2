from MainFrame import MainFrame
from DataFrame import DataFrame
from GraphFrame import GraphFrame
from CountFrame import CountFrame
import pygame

FONT = "C:\\Windows\\Fonts\\msgothic.ttc"

class App:
    def __init__(self, screen):
        self.screen = screen
        self.runnig = True
        print("スクリーンを生成")
        #   スクリーンを辞書に登録
        self.screens = {
            "main" : MainFrame(self.screen, FONT),
            "data" : DataFrame(self.screen, FONT),
            "pass" : MainFrame(self.screen, FONT),
            "count": CountFrame(self.screen, FONT),
            "graph": GraphFrame(self.screen, FONT)
        }
        print("生成完了")
        self.background_image_main = pygame.image.load("box_01/img01.jpg")
        self.background_image_main = pygame.transform.scale(self.background_image_main, (1920,1080))
        self.current_screen = "main"
    
    #   実行
    def run(self):
        while self.runnig:
            if self.current_screen != "end":
                screen = self.screens[self.current_screen]
                action = screen.update()
                if action:
                    self.current_screen = action
                self.screen.blit(self.background_image_main, (0, 0))
                screen.draw()
                
            else:
                self.runnig = False
