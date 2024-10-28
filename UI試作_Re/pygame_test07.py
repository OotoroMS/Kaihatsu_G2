#暗くしたり明るくする
import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Darken Transition Example")

# 背景画像の読み込み
background_image_main = pygame.image.load("box_01/img01.jpg")
background_image_game = pygame.image.load("box_01/img02.jpg")

# 背景画像を画面サイズにリサイズ
background_image_main = pygame.transform.scale(background_image_main, (screen_width, screen_height))
background_image_game = pygame.transform.scale(background_image_game, (screen_width, screen_height))

# 背景色と暗くする色
DARK_COLOR = (0, 0, 0)
DARKEN_DURATION = 15  # 暗くするフレーム数
BRIGHTEN_DURATION = 60  # 明るくするフレーム数

# フォントの設定
font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 40)

# 画面状態を表す定数を定義
MAIN_MENU = "main_menu"
GAME_SCREEN = "game_screen"

# 現在の画面状態を保持する変数
current_screen = MAIN_MENU
next_screen = None  # 次の画面状態
is_transitioning = False  # 遷移中フラグ
darken_alpha = 0  # 暗くする強さ

# ボタンの描画関数
def draw_button(text, x, y, width, height, hover=False):
    button_color = (200, 200, 200) if not hover else (170, 170, 170)
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = button_font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

# メインメニューの描画
def draw_main_menu():
    screen.blit(background_image_main, (0, 0))  # 背景画像を描画
    title_text = font.render("Main Menu", True, (0, 0, 0))
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 3 - title_text.get_height() // 2))
    draw_button("Start Game", screen_width // 2 - 100, screen_height // 2, 200, 60)
    draw_button("Quit", screen_width // 2 - 100, screen_height // 2 + 100, 200, 60)

# ゲーム画面の描画
def draw_game_screen():
    screen.blit(background_image_game, (0, 0))  # 背景画像を描画
    game_text = font.render("Game Screen", True, (255, 255, 255))
    screen.blit(game_text, (screen_width // 2 - game_text.get_width() // 2, screen_height // 3 - game_text.get_height() // 2))
    draw_button("Back to Menu", screen_width // 2 - 150, screen_height // 2, 300, 60)

# ボタンクリック判定
def button_clicked(x, y, width, height, mouse_pos):
    return x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height

# 画面遷移処理
def transition_to_next_screen():
    global is_transitioning, darken_alpha
    is_transitioning = True

    # 暗くなる処理
    for frame in range(DARKEN_DURATION):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        darken_alpha = frame * (255 // DARKEN_DURATION)
        screen.fill((255, 255, 255))  # 白で塗りつぶし
        # 背景を描画
        if current_screen == MAIN_MENU:
            draw_main_menu()
        elif current_screen == GAME_SCREEN:
            draw_game_screen()

        # 暗くなるオーバーレイを描画
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill(DARK_COLOR)
        overlay.set_alpha(darken_alpha)
        screen.blit(overlay, (0, 0))

        pygame.display.flip()
        pygame.time.delay(30)

    # 次の画面を描画
    if next_screen == GAME_SCREEN:
        draw_game_screen()
    elif next_screen == MAIN_MENU:
        draw_main_menu()

    # 明るくなる処理
    for frame in range(DARKEN_DURATION):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 明るくなるオーバーレイを描画
        brighten_alpha = 255 - (frame * (255 // DARKEN_DURATION))
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill(DARK_COLOR)
        overlay.set_alpha(brighten_alpha)
        screen.blit(overlay, (0, 0))

        pygame.display.flip()
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

    if current_screen == MAIN_MENU and not is_transitioning:
        draw_main_menu()

        # ボタンのホバーとクリック処理（Start Game）
        if button_clicked(screen_width // 2 - 100, screen_height // 2, 200, 60, mouse_pos):
            draw_button("Start Game", screen_width // 2 - 100, screen_height // 2, 200, 60, hover=True)
            if mouse_click:
                next_screen = GAME_SCREEN
                transition_to_next_screen()
                current_screen = next_screen
        # ボタンのホバーとクリック処理（Quit）
        elif button_clicked(screen_width // 2 - 100, screen_height // 2 + 100, 200, 60, mouse_pos):
            draw_button("Quit", screen_width // 2 - 100, screen_height // 2 + 100, 200, 60, hover=True)
            if mouse_click:
                pygame.quit()
                sys.exit()
        else:
            draw_button("Start Game", screen_width // 2 - 100, screen_height // 2, 200, 60)
            draw_button("Quit", screen_width // 2 - 100, screen_height // 2 + 100, 200, 60)

    elif current_screen == GAME_SCREEN and not is_transitioning:
        draw_game_screen()

        # ボタンのホバーとクリック処理（Back to Menu）
        if button_clicked(screen_width // 2 - 150, screen_height // 2, 300, 60, mouse_pos):
            draw_button("Back to Menu", screen_width // 2 - 150, screen_height // 2, 300, 60, hover=True)
            if mouse_click:
                next_screen = MAIN_MENU
                transition_to_next_screen()
                current_screen = next_screen
        else:
            draw_button("Back to Menu", screen_width // 2 - 150, screen_height // 2, 300, 60)

    pygame.display.flip()
