#四角形が上下にバウンド
import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Square Animation")

# 色定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 四角形の初期位置とサイズ
rect_x = screen_width // 2 - 50
rect_y = 50
rect_width = 100
rect_height = 100
speed_y = 5

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 背景を塗りつぶす
    screen.fill(WHITE)

    # 四角形を描画
    pygame.draw.rect(screen, RED, (rect_x, rect_y, rect_width, rect_height))

    # 四角形の位置を更新
    rect_y += speed_y
    if rect_y + rect_height > screen_height or rect_y < 0:
        speed_y = -speed_y  # 壁に当たったら逆方向に

    pygame.display.update()

    pygame.time.delay(10)  # 更新間隔を少し遅らせる
