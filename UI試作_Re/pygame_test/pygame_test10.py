#揺れてから拡大縮小で遷移
import pygame
import sys
import random

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Screen Transition with Animations")

# 色の定義 (RGB形式)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# フォントの設定
font = pygame.font.Font(None, 50)

# 画面状態を表す定数を定義
MAIN_MENU = "main_menu"  # メインメニュー画面
GAME_SCREEN = "game_screen"  # ゲーム画面

# 現在の画面状態を保持する変数
current_screen = MAIN_MENU

# メインメニューの描画関数
def draw_main_menu():
    screen.fill(WHITE)  # 背景を白で塗りつぶす
    title_text = font.render("Main Menu", True, BLUE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 3))
    # 「Start Game」ボタンの描画
    start_text = font.render("Start Game", True, BLUE)
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2))
    pygame.display.flip()

# ゲーム画面の描画関数
def draw_game_screen():
    screen.fill(WHITE)  # 背景を白で塗りつぶす
    game_text = font.render("Game Screen", True, BLUE)
    screen.blit(game_text, (screen_width // 2 - game_text.get_width() // 2, screen_height // 3))
    pygame.display.flip()

# 拡大縮小アニメーション
def zoom_out(duration):
    surface = screen.copy()
    for scale in range(100, 0, -2):  # 100%から0%へ
        scaled_surface = pygame.transform.scale(surface, (surface.get_width() * scale // 100, surface.get_height() * scale // 100))
        screen.blit(scaled_surface, (screen_width // 2 - scaled_surface.get_width() // 2, screen_height // 2 - scaled_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(duration // 50)

def zoom_in(duration):
    surface = screen.copy()
    for scale in range(0, 101, 2):  # 0%から100%へ
        scaled_surface = pygame.transform.scale(surface, (surface.get_width() * scale // 100, surface.get_height() * scale // 100))
        screen.blit(scaled_surface, (screen_width // 2 - scaled_surface.get_width() // 2, screen_height // 2 - scaled_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(duration // 50)

# 回転アニメーション
def rotate_in(duration):
    surface = screen.copy()
    for angle in range(0, 361, 5):  # 0°から360°へ
        rotated_surface = pygame.transform.rotate(surface, angle)
        screen.blit(rotated_surface, (screen_width // 2 - rotated_surface.get_width() // 2, screen_height // 2 - rotated_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.delay(duration // 72)  # 72は360/5

# 縦揺れアニメーション
def shake_screen(duration):
    surface = screen.copy()
    for _ in range(duration // 10):
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.blit(surface, (offset_x, offset_y))
        pygame.display.flip()
        pygame.time.delay(10)

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_screen == MAIN_MENU:
        draw_main_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:  # Enterキーでゲーム画面へ
            shake_screen(300)  # 縦揺れアニメーション
            zoom_out(300)      # 拡大縮小アニメーション
            current_screen = GAME_SCREEN
            zoom_in(300)       # ゲーム画面を表示
    elif current_screen == GAME_SCREEN:
        draw_game_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Escキーでメインメニューへ戻る
            shake_screen(300)  # 縦揺れアニメーション
            zoom_out(300)      # 拡大縮小アニメーション
            current_screen = MAIN_MENU
            zoom_in(300)       # メインメニューを表示

pygame.quit()
sys.exit()
