import pygame

pygame.init()

BLACK = (0, 0, 0)

#   ボタンクラス
class Button():
    #   screen:pygameのスクリーン x:x座標の開始位置 y:y座標の開始位置 width:横幅 height:縦幅 color:背景色 text:テキスト text_size:テキストの大きさ action:ボタンに紐づける関数 
    def __init__(self, screen, x, y, width, height, color, text, text_size, action):
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)    #   矩形を生成
        self.color = color
        self.text = text
        self.action = action
        self.font = pygame.font.Font("C:\\Windows\\Fonts\\msgothic.ttc",size=text_size)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)    #   本体を描画
        pygame.draw.rect(self.screen, BLACK, self.rect, 1)      #   外枠を描画
        font = pygame.font.SysFont(None, 36)                    #   フォントを設定
        text_img = self.font.render(self.text, True, BLACK)     #   テキストを生成
        self.screen.blit(text_img,(self.rect.x + 10, self.rect.y + 10)) #   テキストを描画
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action()
