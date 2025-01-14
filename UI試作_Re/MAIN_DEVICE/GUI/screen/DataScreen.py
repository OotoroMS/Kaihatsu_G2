import pygame
import sys
sys.path.append("../MAIN_DEVICE/GUI")
sys.path.append("../MAIN_DEVICE/")
from typing               import Tuple,Optional

# 定数
from GUI.constant.file_path   import *
from GUI.constant.screen_name import *
from GUI.constant.popup_name  import *
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture
from GUI.screen.BaseScreen    import BaseScreen
# データベース接続クラス
from DATABASE.SQLCommunication import SQLCommunication

DATA_TETLE_STATUS    = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_data.png"
}
EXPTXT_DATA_STATUS   = {
    "coordinate" : (175, 600),
    "size"       : (650, 350),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_count.png"
}
EXPTXT_GRAPH_STATUS  = {
    "coordinate" : (1025,600),
    "size"       : (650, 350),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_graph.png"
}
BUTTON_COUNT_STATUS  = {
    "coordinate" : (150, 300),
    "size"       : (700, 350),
    "image_path" : BUTTON_FILE_PATH + "button_count.png"
}
BUTTON_GRAPH_STATUS  = {
    "coordinate" : (1000,300),
    "size"       : (700, 350),
    "image_path" : BUTTON_FILE_PATH + "button_graph.png"
}
BUTTON_BACK_STATUS   = {
    "coordinate" : (0,   960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}

# データ確認用
QUERY = "select * from db_now"

class DataScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.db = SQLCommunication()
    
    # 表示画像設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **DATA_TETLE_STATUS),
            Picture(self.screen, **EXPTXT_DATA_STATUS),
            Picture(self.screen, **EXPTXT_GRAPH_STATUS)
        ]
    
    # 表示ボタン設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_COUNT_STATUS, func=self.move_count),
            Button(self.screen, **BUTTON_GRAPH_STATUS, func=self.move_graph),
            Button(self.screen, **BUTTON_BACK_STATUS,  func=self.back)
        ]
    
    # データ一覧画面に遷移
    def move_count(self):
        result = self.db.db_query_execution(DATABESE, QUERY)
        if result:
            return COUNT, OK
        else:
            print("POPUPに置き換えます。データベースにデータなし")
            return None, NG
    
    # 動作確認画面に遷移
    def move_graph(self):
        return GRAPH, OK
    
    # 終了処理
    def back(self):
        return MAIN, OK