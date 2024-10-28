#画面遷移スライド
import pygame
import sys

# Pygameの初期化
pygame.init()

# 画面サイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Slide Transition with Background")

# 背景画像の読み込みとリサイズ
background_menu = pygame.image.load("box_01/img01.jpg")
background_game = pygame.image.load("box_01/img02.jpg")
background_menu = pygame.transform.scale(background_menu, (screen_width, screen_height))
background_game = pygame.transform.scale(background_game, (screen_width, screen_height))

# フォント
font = pygame.font.Font(None, 50)

# 画面状態の定義
MAIN_MENU = "main_menu"
GAME_SCREEN = "game_screen"

# 現在の画面状態
current_screen = MAIN_MENU
next_screen = None
is_transitioning = False

# スライドアニメーション用の変数
slide_offset = 0
slide_speed = 30

# メインメニューの描画
def draw_main_menu(offset_x=0):
    # 背景画像を描画
    screen.blit(background_menu, (offset_x, 0))
    # テキストを描画
    title_text = font.render("Main Menu", True, (0, 0, 255))
    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2 + offset_x, screen_height//2 - title_text.get_height()//2))

# ゲーム画面の描画
def draw_game_screen(offset_x=0):
    # 背景画像を描画
    screen.blit(background_game, (offset_x, 0))
    # テキストを描画
    game_text = font.render("Game Screen", True, (255, 255, 255))
    screen.blit(game_text, (screen_width//2 - game_text.get_width()//2 + offset_x, screen_height//2 - game_text.get_height()//2))

# 画面遷移の処理
def slide_transition(current, next):
    global slide_offset, is_transitioning

    # スライドアニメーションを開始する
    slide_offset = 0
    is_transitioning = True

    while slide_offset < screen_width:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 現在の画面を左にスライド
        if current == MAIN_MENU:
            draw_main_menu(-slide_offset)
        elif current == GAME_SCREEN:
            draw_game_screen(-slide_offset)

        # 次の画面を右からスライドイン
        if next == MAIN_MENU:
            draw_main_menu(screen_width - slide_offset)
        elif next == GAME_SCREEN:
            draw_game_screen(screen_width - slide_offset)

        pygame.display.update()

        slide_offset += slide_speed
        pygame.time.delay(30)

    is_transitioning = False

# メインループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # 画面遷移のトリガー (スペースキーを押すと画面遷移)
        if event.type == pygame.KEYDOWN and not is_transitioning:
            if event.key == pygame.K_SPACE:
                if current_screen == MAIN_MENU:
                    next_screen = GAME_SCREEN
                elif current_screen == GAME_SCREEN:
                    next_screen = MAIN_MENU

                # スライドアニメーションを実行
                slide_transition(current_screen, next_screen)

                # 画面遷移を完了する
                current_screen = next_screen

    # 現在の画面の描画（遷移中でないとき）
    if not is_transitioning:
        if current_screen == MAIN_MENU:
            draw_main_menu()
        elif current_screen == GAME_SCREEN:
            draw_game_screen()

    pygame.display.update()
    pygame.time.delay(30)
