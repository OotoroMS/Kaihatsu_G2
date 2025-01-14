# 寸法検査の測定値グラフを表示する画面
# 現在は遷移時のみ更新するようになっている
import pygame
import sys
import os
sys.path.append("../MAIN_DEVICE/GUI")
sys.path.append("../MAIN_DEVICE/")
from typing               import Tuple,Optional

# 定数
from GUI.constant.file_path    import *
from GUI.constant.screen_name  import *
from GUI.constant.popup_name   import *
# 部品
import GUI.parts.Graph         as     Graph
from   GUI.parts.Button        import Button
from   GUI.parts.Picture       import Picture
# 画面
from GUI.screen.BaseScreen     import BaseScreen
# データベース接続クラス
from DATABASE.SQLCommunication import SQLCommunication

# グラフの大きさ
GRAPH_SIZE = (1500, 700)
# グラフの座標
GRAPH_COODINATE = (200, 200)
# 各種部品の設定
TITLE_GRAPH_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_graph.png"
}
BUTTON_BACK_STATUS = {
    "coordinate" : (0,   960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
# NO_IMAGEのファイルパス
NO_IMAGE_FILE_PATH = EXPTXT_FILE_PATH + "exptxt_no_image.png"
# グラフ生成フラグ
ON  = True
OFF = False


class GraphScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.graph_create_frag = ON
        self.graph             = None
        self.graph_image       = None
    # ボタンの設定
    def setting_buttons(self):
        self.buttons = {
            Button(self.screen, **BUTTON_BACK_STATUS, func=self.move_data)
        }
    # 画像の設定
    def setting_images(self):
        self.images = {
            Picture(self.screen, **TITLE_GRAPH_STATUS)
        }
    
    # 描画
    def draw(self):
        for image  in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        self.draw_graph()
        if self.graph_image:
            self.screen.blit(self.graph_image, GRAPH_COODINATE)
        
    # グラフ描画・更新処理
    def draw_graph(self):
        if self.graph_create_frag:
            self.graph_create_frag = OFF
            Graph.graph()
            self.load_graph()
            self.resaize_image()
    
    # 生成したグラフを読み込む
    def load_graph(self):
        if os.path.exists(GRAPH_IMAGE_PATH):
            self.graph = pygame.image.load(GRAPH_IMAGE_PATH)
        else:
            self.graph = NO_IMAGE_FILE_PATH

    def resaize_image(self):
        if self.graph:
            self.graph_image = pygame.transform.scale(self.graph, GRAPH_SIZE)

    def move_data(self):
        self.graph_create_frag = ON
        return DATA, OK