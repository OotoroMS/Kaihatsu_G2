# GUI/FRONT/parts/Button.py

import pygame
from typing import Tuple

class Text:
    def __init__(self, screen: pygame.Surface, pos: Tuple[int, int], 
                 text: str, color: tuple[int, int, int],
                 font: pygame.font.Font):
        self.screen: pygame.Surface = screen    # ボタンを置く画面
        self.pos: tuple[int, int] = pos  # テキストの座標
        text    # テキストの内容
        self.color: tuple[int, int, int] = color   # テキストの色
        self.font: pygame.font.Font = font   # テキストのフォント
        # ここでテキストの作成
        lines: list[str] = text.split('\n')   # 改行で分割して行ごとに保存
        self.view_text: list[pygame.Surface] = [] # 各行のテキストをリストに保存
        self.text(lines, color, font)
    
    def text(self, lines: list[str], color: tuple[int, int, int],
             font: pygame.font.Font):
        for line in lines:
            self.view_text.append(font.render(line, True, color))
    
    # ボタン描画
    def draw(self):
        x, y = self.pos
        for text in self.view_text:
            text_width = text.get_width()
            x_center = x - text_width // 2            
            self.screen.blit(text, (x_center, y))
            y += self.font.get_linesize() # 次の行に移動

    def update(self, text: str):
        lines: list[str] = text.split('\n')
        # 一度初期化
        self.view_text = []
        for line in lines:
            self.view_text.append(self.font.render(line, True, self.color))
