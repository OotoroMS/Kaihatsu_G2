import pygame
from typing import Tuple, Optional
# ベースクラス
from GUI.popup.BasePopup import BasePopup
# 定数
from GUI.constant.file_path  import *
from GUI.constant.popup.popup_name import *
from GUI.constant.color      import *
from GUI.constant.popup.popup_text import *
from GUI.constant.normal     import *
# 部品
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture

QUERY = "DELETE FROM %s"
TARGETTABLE = [
    "db_now",
    "db_countlog",
    "db_timelog",
    "db_sizelog"
]

class ResetPopup(BasePopup):
    def __init__(self, screen: pygame.Surface, text_index : str) -> None:
        super().__init__(screen)
        self.setting_text(text_index)

    # テキストを生成
    def setting_text(self, text_index):
        if text_index in POPUP_TEXT.keys():
            # 表示用テキストを生成
            self.view_text = self.text_font.render(POPUP_TEXT[text_index], True, WHITE)

    # ボタンの設定
    def setting_buttons(self):
        button_width  = self.width  // 4
        button_height = self.height // 4
        button_yes_x  = self.pos_x + (self.width // 2) + (button_width // 2)
        button_no_x   = self.pos_x + (button_width // 2)
        button_y      = self.height - (self.height // 4)
        self.buttons = [
            Button(self.screen, (button_yes_x, button_y), (button_width, button_height), BUTTON_FILE_PATH +"pic77.png", self.no),
            Button(self.screen, (button_no_x, button_y), (button_width, button_height), BUTTON_FILE_PATH +"pic76.png", self.yes)
        ]

    # 描画処理
    def draw(self):
        super().draw()
        width  = self.view_text.get_width()
        height = self.view_text.get_height()
        x = self.pos_x + (self.width  // 2) - (width // 2)
        y = (self.height // 2) - (height // 2)
        self.screen.blit(self.view_text, (x, y))

    # ボタンのイベント処理
    def yes(self):
        for table in TARGETTABLE:
            delete_query = QUERY % table
            print(delete_query)
            # print("変更前")
            # self.db.table_data_list_display(table_name=table)
            # self.db.db_query_execution(query=delete_query)
            # print("変更後")
            # self.db.table_data_list_display(table_name=table)
        return True, OK
        return DB_RESET, OK
    
    def no(self):
        return False, OK