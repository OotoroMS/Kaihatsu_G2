import pygame
from pygame.locals import *
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("test")
    font = pygame.font.Font(None, 55)
    while (1):
        # screen.fill((0,0,0))                                    # 画面を黒色に塗りつぶし
        # text = font.render("TEST", True, (255,255,255))   # 描画する文字列の設定
        # screen.blit(text, [20, 100])# 文字列の表示位置
        # pygame.display.update()     # 画面を更新
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
if __name__ == '__main__':
    main()