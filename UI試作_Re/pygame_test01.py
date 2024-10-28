#ボタンとテキストボックス
import pygame
import sys

# Pygameの初期化
pygame.init()

# ウィンドウサイズ
WIDTH, HEIGHT = 1900, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame GUI Example')

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# フォント設定
font = pygame.font.Font(None, 36)

# テキストボックスクラス
class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = WHITE
        self.text = ''
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

# ボタンのクラス
class Button:
    def __init__(self, x, y, width, height, shape, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.shape = shape
        self.color = color
        self.text = text

    def draw(self, screen):
        if self.shape == 'rectangle':
            pygame.draw.rect(screen, self.color, self.rect)
        elif self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2), self.rect.width // 2)
        elif self.shape == 'polygon':
            pygame.draw.polygon(screen, self.color, [(self.rect.x, self.rect.y + self.rect.height),
                                                       (self.rect.x + self.rect.width // 2, self.rect.y),
                                                       (self.rect.x + self.rect.width, self.rect.y + self.rect.height)])

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# ボタンとテキストボックスの作成
text_box = TextBox(50, 50, 200, 40)
buttons = [
    Button(300, 50, 100, 50, 'rectangle', RED, 'Rectangle'),
    Button(450, 50, 100, 50, 'circle', GREEN, 'Circle'),
    Button(600, 50, 100, 50, 'polygon', BLUE, 'Polygon')
]

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        text_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    print(f"{button.text} button clicked!")

    # 背景の描画
    screen.fill((169,169,169))

    # ボタンとテキストボックスの描画
    for button in buttons:
        button.draw(screen)
    text_box.draw(screen)

    # 画面の更新
    pygame.display.flip()
