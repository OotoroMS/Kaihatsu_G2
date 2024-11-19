import pygame

pygame.init()

BLACK = (0, 0, 0)

#   ボタンクラス
class Button():
    #   screen:pygameのスクリーン x:x座標の開始位置 y:y座標の開始位置 width:横幅 height:縦幅 color:背景色 text:テキスト text_size:テキストの大きさ action:ボタンに紐づける関数 
    def __init__(self, screen, x, y, width, height, image_path, action):
        self.screen = screen
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.base_image = pygame.image.load(image_path)
        self.default_button()
        self.action = action
        self.hover_scale = 1.1

    #   描画処理
    def draw(self):
        self.hover_button()
        self.screen.blit(self.image, self.rect) #   テキストを描画
    
    def expansion_button(self):
        x = self.x - (self.width * (self.hover_scale - 1)) // 2
        y = self.y - (self.height * (self.hover_scale - 1)) // 2
        width = self.width * self.hover_scale
        height = self.height * self.hover_scale
        self.image = pygame.transform.scale(self.base_image,(width, height))
        rect = self.image.get_rect()
        rect.topleft = (x, y)
        self.rect = rect
    
    def default_button(self):
        self.image = pygame.transform.scale(self.base_image,(self.width, self.height))
        self.base_rect = self.image.get_rect()
        self.base_rect.topleft = (self.x, self.y)
        self.rect = self.base_rect
    
    #   ボタンのアニメーション処理
    def hover_button(self):
        pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(pos)
        if hovered:
            self.expansion_button()
        else:
            self.default_button()

    #   押下処理
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action()
