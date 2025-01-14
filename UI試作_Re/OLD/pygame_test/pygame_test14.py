#回転扉みたいな遷移
import pygame
import sys
import math

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("3D Cube Rotation Transition")

# フォント設定
font = pygame.font.Font(None, 60)

# 背景色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 各画面の定数
MAIN_MENU = "main_menu"
GAME_SCREEN = "game_screen"
current_screen = MAIN_MENU

# 背景画像の読み込みとサイズ変更
background_image_main = pygame.image.load("box_01/img01.jpg")
background_image_main = pygame.transform.scale(background_image_main, (screen_width, screen_height))

background_image_game = pygame.image.load("box_01/img02.jpg")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))

# ボタンの描画関数
def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# メインメニュー画面の描画
def draw_main_menu():
    screen.blit(background_image_main, (0, 0))
    draw_button("Start Game", screen_width // 2 - 100, screen_height // 2 - 30, 200, 60, BLACK)

# ゲーム画面の描画
def draw_game_screen():
    screen.blit(background_image_game, (0, 0))
    draw_button("Back to Menu", screen_width // 2 - 100, screen_height // 2 - 30, 200, 60, BLACK)

# 3D回転風画面遷移
def cube_rotation_transition(current_surface, next_surface):
    for frame in range(0, 91, 5):  # 0度から90度まで5度ずつ回転
        angle_rad = math.radians(frame)
        scale_factor = abs(math.cos(angle_rad))  # 回転に伴う縮小・拡大を計算

        # 現在の画面のスケーリング
        scaled_current = pygame.transform.scale(current_surface, 
                                                (int(screen_width * scale_factor), screen_height))
        current_rect = scaled_current.get_rect(center=(screen_width // 2, screen_height // 2))

        # 次の画面のスケーリング
        scaled_next = pygame.transform.scale(next_surface, 
                                             (int(screen_width * (1 - scale_factor)), screen_height))
        next_rect = scaled_next.get_rect(center=(screen_width // 2, screen_height // 2))

        # 描画
        screen.fill(BLACK)
        if frame < 45:  # 最初は現在の画面が縮小
            screen.blit(scaled_current, current_rect)
        else:  # 45度を超えたら次の画面が拡大
            screen.blit(scaled_next, next_rect)

        pygame.display.flip()
        pygame.time.delay(30)  # アニメーションの速度を調整

# メインループ
running = True
while running:
    screen.fill(WHITE)

    # 現在の画面に応じて描画
    if current_screen == MAIN_MENU:
        draw_main_menu()
    elif current_screen == GAME_SCREEN:
        draw_game_screen()

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # ボタンのクリック判定
            if current_screen == MAIN_MENU and screen_width // 2 - 100 <= mouse_pos[0] <= screen_width // 2 + 100 and screen_height // 2 - 30 <= mouse_pos[1] <= screen_height // 2 + 30:
                # メインメニューからゲーム画面への遷移
                main_menu_surface = screen.copy()
                game_screen_surface = pygame.Surface((screen_width, screen_height))
                draw_game_screen()
                game_screen_surface.blit(screen, (0, 0))
                cube_rotation_transition(main_menu_surface, game_screen_surface)
                current_screen = GAME_SCREEN

            elif current_screen == GAME_SCREEN and screen_width // 2 - 100 <= mouse_pos[0] <= screen_width // 2 + 100 and screen_height // 2 - 30 <= mouse_pos[1] <= screen_height // 2 + 30:
                # ゲーム画面からメインメニューへの遷移
                game_screen_surface = screen.copy()
                main_menu_surface = pygame.Surface((screen_width, screen_height))
                draw_main_menu()
                main_menu_surface.blit(screen, (0, 0))
                cube_rotation_transition(game_screen_surface, main_menu_surface)
                current_screen = MAIN_MENU

    # 画面更新
    pygame.display.update()

