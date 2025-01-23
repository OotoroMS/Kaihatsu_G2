import pygame
from typing import Tuple, Optional
# ベースクラス
from MAIN_OPRATION.GUI.Popups.BasePopup import BasePopup
# 定数
from MAIN_OPRATION.GUI.Constants.file_path  import *
from MAIN_OPRATION.GUI.Constants.popup_name import *
from MAIN_OPRATION.GUI.Constants.color      import *
from MAIN_OPRATION.GUI.Constants.popup_text import *
from MAIN_OPRATION.GUI.Constants.normal     import *
# 部品
from MAIN_OPRATION.GUI.Parts.Button         import Button
from MAIN_OPRATION.GUI.Parts.Picture        import Picture

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
            Button(self.screen, (button_yes_x, button_y), (button_width, button_height), BUTTON_FILE_PATH +"button_end.png", self.no),
            Button(self.screen, (button_no_x, button_y), (button_width, button_height), BUTTON_FILE_PATH +"button_back.png", self.yes)
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