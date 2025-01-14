#任意の場所に線を引くプログラム
import pygame
import sys

# 初期化
pygame.init()

# 画面のサイズを設定
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("線を引くプログラム")

# 色の設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 変数初期化
start_pos = None
end_pos = None
screen.fill(WHITE)
# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 線の開始位置を設定
            start_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            # 線の終了位置を設定
            end_pos = event.pos
            # 画面に線を描画
            pygame.draw.line(screen, BLACK, start_pos, end_pos, 2)
            start_pos = None
            end_pos = None

    # 画面の更新
    pygame.display.flip()

    # 画面を白でクリア（線を残したい場合は消去しないようにする）
    #screen.fill(WHITE)
