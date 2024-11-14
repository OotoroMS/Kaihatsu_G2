#画像を表示させる設定
import pygame

pygame.init()

BLACK = (0, 0, 0)

#   ピクチャークラス
class Picture():
    #   screen:pygameのスクリーン x:x座標の開始位置 y:y座標の開始位置 width:横幅 height:縦幅 color:背景色 text:テキスト text_size:テキストの大きさ action:ボタンに紐づける関数 
    def __init__(self, screen, x, y, width, height, image_path):
        self.screen = screen
        self.base_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.base_image,(width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    #   描画処理
    def draw(self):
        self.screen.blit(self.image, self.rect) #   テキストを描画
    
