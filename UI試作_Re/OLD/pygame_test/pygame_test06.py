#スライド改良 上下左右_画面遷移
import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slide Transition with Multi-direction")

# 背景画像の読み込みとサイズ変更
background_image_main = pygame.image.load("box_01/img01.jpg")
background_image_main = pygame.transform.scale(background_image_main, (screen_width, screen_height))

background_image_game = pygame.image.load("box_01/img02.jpg")
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))

background_image_settings = pygame.image.load("box_01/img03.jpg")
background_image_settings = pygame.transform.scale(background_image_settings, (screen_width, screen_height))

# 色定義
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)

# フォント
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 40)

# 画面状態の定義
MAIN_MENU = "main_menu"
GAME_SCREEN = "game_screen"
SETTINGS_SCREEN = "settings_screen"

# 現在の画面状態
current_screen = MAIN_MENU
next_screen = None
is_transitioning = False

# スライドアニメーション用の変数
slide_duration = 30  # スライドのフレーム数（アニメーションの長さ）

# イージング関数 (イーズイン・イーズアウト)
def ease_in_out_quad(t, b, c, d):
    t /= d / 2
    if t < 1:
        return c / 2 * t * t + b
    t -= 1
    return -c / 2 * (t * (t - 2) - 1) + b

# ボタンの描画関数
def draw_button(text, x, y, width, height, hover=False):
    button_color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = button_font.render(text, True, BLUE)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# メインメニューの描画
def draw_main_menu(offset_x=0, offset_y=0):
    screen.blit(background_image_main, (offset_x, offset_y))
    title_text = font.render("Main Menu", True, BLUE)
    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2 + offset_x, screen_height//3 - title_text.get_height()//2 + offset_y))
    draw_button("Start Game", screen_width//2 - 100 + offset_x, screen_height//2 + offset_y, 200, 60)
    draw_button("Settings", screen_width//2 - 100 + offset_x, screen_height//2 + 100 + offset_y, 200, 60)

# ゲーム画面の描画
def draw_game_screen(offset_x=0, offset_y=0):
    screen.blit(background_image_game, (offset_x, offset_y))
    game_text = font.render("Game Screen", True, WHITE)
    screen.blit(game_text, (screen_width//2 - game_text.get_width()//2 + offset_x, screen_height//3 - game_text.get_height()//2 + offset_y))
    draw_button("Back to Menu", screen_width//2 - 150 + offset_x, screen_height//2 + offset_y, 300, 60)

# 設定画面の描画
def draw_settings_screen(offset_x=0, offset_y=0):
    screen.blit(background_image_settings, (offset_x, offset_y))
    settings_text = font.render("Settings", True, WHITE)
    screen.blit(settings_text, (screen_width//2 - settings_text.get_width()//2 + offset_x, screen_height//3 - settings_text.get_height()//2 + offset_y))
    draw_button("Back to Menu", screen_width//2 - 150 + offset_x, screen_height//2 + offset_y, 300, 60)

# ボタンクリック判定
def button_clicked(x, y, width, height, mouse_pos):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

# 画面遷移の処理（イージングを使ったスライドアニメーション）
def slide_transition(current, next, direction="right"):
    global is_transitioning
    is_transitioning = True

    for frame in range(slide_duration + 1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # イージングを使ってスライド量を計算
        slide_offset = ease_in_out_quad(frame, 0, screen_width, slide_duration) if direction in ["right", "left"] else ease_in_out_quad(frame, 0, screen_height, slide_duration)

        if direction == "right":
            # 右にスライド
            if current == MAIN_MENU:
                draw_main_menu(-slide_offset)
            elif current == GAME_SCREEN:
                draw_game_screen(-slide_offset)

            if next == MAIN_MENU:
                draw_main_menu(screen_width - slide_offset)
            elif next == GAME_SCREEN:
                draw_game_screen(screen_width - slide_offset)
        elif direction == "left":
            # 左にスライド
            if current == MAIN_MENU:
                draw_main_menu(slide_offset)
            elif current == GAME_SCREEN:
                draw_game_screen(slide_offset)

            if next == MAIN_MENU:
                draw_main_menu(-screen_width + slide_offset)
            elif next == GAME_SCREEN:
                draw_game_screen(-screen_width + slide_offset)
        elif direction == "down":
            # 下にスライド
            if current == MAIN_MENU:
                draw_main_menu(0, -slide_offset)
            elif current == SETTINGS_SCREEN:
                draw_settings_screen(0, -slide_offset)

            if next == MAIN_MENU:
                draw_main_menu(0, screen_height - slide_offset)
            elif next == SETTINGS_SCREEN:
                draw_settings_screen(0, screen_height - slide_offset)
        elif direction == "up":
            # 上にスライド
            if current == MAIN_MENU:
                draw_main_menu(0, slide_offset)
            elif current == SETTINGS_SCREEN:
                draw_settings_screen(0, slide_offset)

            if next == MAIN_MENU:
                draw_main_menu(0, -screen_height + slide_offset)
            elif next == SETTINGS_SCREEN:
                draw_settings_screen(0, -screen_height + slide_offset)

        pygame.display.update()
        pygame.time.delay(30)

    is_transitioning = False

# メインループ
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

    # 現在の画面に応じた処理
    if current_screen == MAIN_MENU and not is_transitioning:
        draw_main_menu()

        # ボタンのホバーとクリック処理（Start Game）
        if button_clicked(screen_width//2 - 100, screen_height//2, 200, 60, mouse_pos):
            draw_button("Start Game", screen_width//2 - 100, screen_height//2, 200, 60, hover=True)
            if mouse_click:
                next_screen = GAME_SCREEN
                slide_transition(current_screen, next_screen, direction="right")
                current_screen = next_screen
        # ボタンのホバーとクリック処理（Settings）
        elif button_clicked(screen_width//2 - 100, screen_height//2 + 100, 200, 60, mouse_pos):
            draw_button("Settings", screen_width//2 - 100, screen_height//2 + 100, 200, 60, hover=True)
            if mouse_click:
                next_screen = SETTINGS_SCREEN
                slide_transition(current_screen, next_screen, direction="down")
                current_screen = next_screen
        else:
            draw_button("Start Game", screen_width//2 - 100, screen_height//2, 200, 60)
            draw_button("Settings", screen_width//2 - 100, screen_height//2 + 100, 200, 60)

    elif current_screen == GAME_SCREEN and not is_transitioning:
        draw_game_screen()

        # ボタンのホバーとクリック処理（Back to Menu）
        if button_clicked(screen_width//2 - 150, screen_height//2, 300, 60, mouse_pos):
            draw_button("Back to Menu", screen_width//2 - 150, screen_height//2, 300, 60, hover=True)
            if mouse_click:
                next_screen = MAIN_MENU
                slide_transition(current_screen, next_screen, direction="left")
                current_screen = next_screen
        else:
            draw_button("Back to Menu", screen_width//2 - 150, screen_height//2, 300, 60)

    elif current_screen == SETTINGS_SCREEN and not is_transitioning:
        draw_settings_screen()

        # ボタンのホバーとクリック処理（Back to Menu）
        if button_clicked(screen_width//2 - 150, screen_height//2, 300, 60, mouse_pos):
            draw_button("Back to Menu", screen_width//2 - 150, screen_height//2, 300, 60, hover=True)
            if mouse_click:
                next_screen = MAIN_MENU
                slide_transition(current_screen, next_screen, direction="up")
                current_screen = next_screen
        else:
            draw_button("Back to Menu", screen_width//2 - 150, screen_height//2, 300, 60)

    pygame.display.update()
    pygame.time.delay(30)