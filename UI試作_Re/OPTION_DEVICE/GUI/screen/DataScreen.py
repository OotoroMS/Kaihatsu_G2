import pygame

# 定数
from GUI.constant.file_path             import *
from GUI.constant.screen.data_constant  import *
from GUI.constant.screen.screen_name    import *
from GUI.constant.popup.popup_name      import *
from GUI.parts.Button                   import Button
from GUI.parts.Picture                  import Picture
from GUI.screen.BaseScreen              import BaseScreen
# データベース接続
from DATABESE.SQLCommunication import SQLCommunication

class DataScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.db = SQLCommunication()
    
    # 表示画像設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **DATA_TETLE_STATUS),
            Picture(self.screen, **EXPTXT_DATA_STATUS),
            Picture(self.screen, **EXPTXT_VISION_STATUS)
        ]
    
    # 表示ボタン設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_COUNT_STATUS, func=self.move_count),
            Button(self.screen, **BUTTON_VISION_STATUS, func=self.move_graph),
            Button(self.screen, **BUTTON_BACK_STATUS,  func=self.back)
        ]
    
    # データ一覧画面に遷移
    def move_count(self):
        result = self.db.db_query_execution(DATABESE, QUERY)
        if result:
            return DATA_COUNT, OK
        else:
            print("POPUPに置き換えます。データベースにデータなし")
            return None, NG
    
    # 動作確認画面に遷移
    def move_graph(self):
        return DATA_VISION, OK
    
    # 終了処理
    def back(self):
        return MAIN, OK