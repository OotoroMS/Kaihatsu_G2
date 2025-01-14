#回転アニメーション見ずらい　おそらく不採用
import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Screen Transition with Rotation Animation")

# 色の定義 (RGB形式)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# フォントの設定
font = pygame.font.Font(None, 50)

# 画面状態を表す定数を定義
MAIN_MENU = "main_menu"  # メインメニュー画面
GAME_SCREEN = "game_screen"  # ゲーム画面

# 背景画像の読み込み
background_image_menu = pygame.image.load("box_01/img01.jpg")  # メインメニューの背景
background_image_game = pygame.image.load("box_01/img02.jpg")  # ゲーム画面の背景

# 現在の画面状態を保持する変数
current_screen = MAIN_MENU

# メインメニューの描画関数
def draw_main_menu():
    screen.blit(background_image_menu, (0, 0))  # 背景を描画
    title_text = font.render("Main Menu", True, BLUE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 3))
    # 「Start Game」ボタンの描画
    start_text = font.render("Start Game", True, BLUE)
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(start_text, start_rect)
    return start_rect  # ボタンの矩形を返す

# ゲーム画面の描画関数
def draw_game_screen():
    screen.blit(background_image_game, (0, 0))  # 背景を描画
    game_text = font.render("Game Screen", True, BLUE)
    screen.blit(game_text, (screen_width // 2 - game_text.get_width() // 2, screen_height // 3))
    # 「Back to Menu」ボタンの描画
    back_text = font.render("Back to Menu", True, BLUE)
    back_rect = back_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(back_text, back_rect)
    return back_rect  # ボタンの矩形を返す

# 回転アニメーション
def rotate_animation(duration):
    surface = screen.copy()
    for angle in range(0, 360, 5):  # 0度から360度まで5度ずつ回転
        rotated_surface = pygame.transform.rotate(surface, angle)
        new_rect = rotated_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(rotated_surface, new_rect.topleft)
        pygame.display.flip()
        pygame.time.delay(duration // 72)  # フレーム間の待機時間を調整

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_screen == MAIN_MENU:
        start_rect = draw_main_menu()
        pygame.display.flip()

        # ボタン操作
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左クリック
            if start_rect.collidepoint(mouse_pos):  # ボタンがクリックされた
                rotate_animation(300)  # 回転アニメーション
                current_screen = GAME_SCREEN  # ゲーム画面へ移動

    elif current_screen == GAME_SCREEN:
        back_rect = draw_game_screen()
        pygame.display.flip()

        # ボタン操作
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左クリック
            if back_rect.collidepoint(mouse_pos):  # ボタンがクリックされた
                rotate_animation(300)  # 回転アニメーション
                current_screen = MAIN_MENU  # メインメニューへ戻る

pygame.quit()
sys.exit()
