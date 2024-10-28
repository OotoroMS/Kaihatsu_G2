#小さいのが右から出てくる
import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("3D Slide Transition")

# 背景画像の読み込みとサイズ変更
background_image_1 = pygame.image.load("box_01/img01.jpg")
background_image_1 = pygame.transform.scale(background_image_1, (screen_width, screen_height))

background_image_2 = pygame.image.load("box_01/img02.jpg")
background_image_2 = pygame.transform.scale(background_image_2, (screen_width, screen_height))

# 3Dスライド遷移の関数
def three_d_slide_transition(current_surface, next_surface, duration=10):
    for frame in range(duration):
        # スライド進行度 (0.0から1.0まで)
        t = frame / duration

        # 現在の画面を縮小し、左に移動
        scale_current = 1 - t * 0.5  # 縮小する割合
        scaled_current = pygame.transform.scale(current_surface, (int(screen_width * scale_current), int(screen_height * scale_current)))
        current_x = -t * screen_width * 0.5  # 左に移動する量

        # 次の画面を拡大し、右から出現
        scale_next = 0.5 + t * 0.5  # 拡大する割合
        scaled_next = pygame.transform.scale(next_surface, (int(screen_width * scale_next), int(screen_height * scale_next)))
        next_x = (1 - t) * screen_width * 0.5  # 右に移動する量

        # 画面のクリア
        screen.fill((0, 0, 0))

        # 現在の画面を描画
        screen.blit(scaled_current, (int(current_x), (screen_height - scaled_current.get_height()) // 2))

        # 次の画面を描画
        screen.blit(scaled_next, (int(next_x), (screen_height - scaled_next.get_height()) // 2))

        # 描画を更新
        pygame.display.update()
        pygame.time.delay(30)  # 遷移速度を調整

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
                    three_d_slide_transition(background_image_1, background_image_2)
                    current_screen = 2
                else:
                    three_d_slide_transition(background_image_2, background_image_1)
                    current_screen = 1

    # 現在の画面を描画
    if current_screen == 1:
        screen.blit(background_image_1, (0, 0))
    else:
        screen.blit(background_image_2, (0, 0))

    pygame.display.update()
