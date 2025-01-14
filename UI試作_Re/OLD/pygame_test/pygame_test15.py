#ページが異なるスピードでスライド遷移する
import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Perspective Scroll Transition")

# 色の定義 (RGB形式)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 背景画像の読み込みとサイズ変更
background_image_1 = pygame.image.load("box_01/img01.jpg")
background_image_1 = pygame.transform.scale(background_image_1, (screen_width, screen_height))

background_image_2 = pygame.image.load("box_01/img02.jpg")
background_image_2 = pygame.transform.scale(background_image_2, (screen_width, screen_height))

# パースペクティブスクロールの遷移
def perspective_scroll_transition(current_surface, next_surface, duration=60):
    for frame in range(duration):
        scroll_factor = frame / duration

        # 背景を異なる速度でスクロール
        current_scroll_x = int(screen_width * scroll_factor * 0.5)  # 背景を遅くスクロール
        next_scroll_x = int(screen_width * scroll_factor * 1.0)    # 前景を速くスクロール

        # 画面をクリア
        screen.fill(BLACK)

        # 現在の画面（背景1）を左にスクロール
        screen.blit(current_surface, (-current_scroll_x, 0))
        
        # 次の画面（背景2）を右にスクロール
        screen.blit(next_surface, (screen_width - next_scroll_x, 0))

        # 描画を更新
        pygame.display.update()
        pygame.time.delay(30)  # フレームレートを調整

# メインループ
running = True
current_screen = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # Enterキーで画面遷移
            if event.key == pygame.K_RETURN:
                if current_screen == 1:
                    perspective_scroll_transition(background_image_1, background_image_2)
                    current_screen = 2
                else:
                    perspective_scroll_transition(background_image_2, background_image_1)
                    current_screen = 1

    # 現在の画面を描画
    if current_screen == 1:
        screen.blit(background_image_1, (0, 0))
    else:
        screen.blit(background_image_2, (0, 0))

    pygame.display.update()
