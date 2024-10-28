import pygame
import shutil
import os
from BaseFrame import BaseFrame
from Button import Button
import Graph

BRACK = ((0,0,0))
WHITE = ((255,255,255))
RED = ((255,0,0))

class GraphFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen)
        self.font = pygame.font.Font(font, 60)
        self.title_text = self.font.render("寸法検査ログ", True, BRACK)
        self.graph_image = None
        self.copy_num = 1
        #   ボタンクラス
        self.buttons = {
            0   : Button(self.screen, 1570, 930, 300, 100, WHITE, "戻る", 90, self.move_data)
        }

    #   イベント処理を記述
    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.buttons:
                    move = self.buttons[i].is_clicked(event)
                    if move:
                        break
                return move
    
    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        #self.screen.fill((255,255,255))
        self.screen.blit(self.title_text,(200,50))
        self.draw_graph()
        for i in self.buttons:
            self.buttons[i].draw()
        pygame.display.update()

    #   グラフを描画
    def draw_graph(self):
        #   グラフの画像を生成
        Graph.create_graph()
        #   グラフの画像があれば
        if os.path.exists("D:\\GitHub\\Kaihatsu_G2\\UI試作_Re\\test_表追加\\graph.png"):
            copy_path = "D:\\GitHub\\Kaihatsu_G2\\UI試作_Re\\test_表追加\\graph"+ str(self.copy_num) + ".png" #   コピー画像のパスを生成
            while True:
                #   パスの画像があれば削除
                if os.path.exists(copy_path):
                    os.remove(copy_path)
                #   コピーを生成
                shutil.copy("D:\\GitHub\\Kaihatsu_G2\\UI試作_Re\\test_表追加\\graph.png",copy_path)
                #   コピー画像が無事に生成できていれば
                if os.path.exists(copy_path):
                    try:
                        self.graph_image = pygame.image.load(copy_path) #   画像を読み込む
                        break   #   ループ終了
                    except pygame.error as e:   #   画像がうまくよみこめなければエラーメッセージを表示してコピーからやり直す
                        pass
                        # print(f"画像のロードに失敗しました: {e}")
            #   生成した画像を画面に描画する 
            self.graph_image = pygame.transform.scale(self.graph_image,(1100,900))
            self.screen.blit(self.graph_image, (100,120))
        #   念のために作成するコピーを1→2→1…と切り替える
        self.copy_num += 1
        if self.copy_num == 3:
            self.copy_num = 1
    
    #   メインメニューに遷移
    def move_data(self):
        return "data"