import pygame
import sys

# Pygameの初期化
pygame.init()

# ウィンドウサイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Icon Button Example')

# 色定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# フォント設定
font = pygame.font.Font(None, 36)

# ボタンのクラス
class IconButton:
    def __init__(self, x, y, size, color, icon_type):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.icon_type = icon_type

    def draw(self, screen):
        if self.icon_type == 'circle':
            pygame.draw.circle(screen, self.color, self.rect.center, self.rect.width // 2)
        elif self.icon_type == 'star':
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.centerx + 20, self.rect.bottom),
                (self.rect.left, self.rect.centery),
                (self.rect.right, self.rect.centery),
                (self.rect.centerx - 20, self.rect.bottom)
            ]
            pygame.draw.polygon(screen, self.color, points)
        elif self.icon_type == 'heart':
            pygame.draw.polygon(screen, self.color, [
                (self.rect.centerx, self.rect.bottom),
                (self.rect.left, self.rect.centery),
                (self.rect.centerx, self.rect.top),
                (self.rect.right, self.rect.centery)
            ])

        # アイコンのテキスト
        text_surface = font.render(self.icon_type.capitalize(), True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# アイコンボタンの作成
buttons = [
    IconButton(100, 100, 100, RED, 'circle'),
    IconButton(250, 100, 100, GREEN, 'star'),
    IconButton(400, 100, 100, BLUE, 'heart'),
]

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.is_clicked(event.pos):
                    print(f"{button.icon_type.capitalize()} button clicked!")

    # 背景の描画
    screen.fill(WHITE)

    # アイコンボタンの描画
    for button in buttons:
        button.draw(screen)

    # 画面の更新
    pygame.display.flip()
