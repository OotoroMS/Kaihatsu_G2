import pygame
import csv
from typing import Tuple, Optional
# ベースクラス
from GUI.popup.BasePopup import BasePopup
# DB接続
from DATABASE.SQLCommunication  import SQLCommunication
# 定数
from GUI.constant.file_path  import *
from GUI.constant.popup_name import *
from GUI.constant.color      import *
from GUI.constant.popup_text import *
from GUI.constant.normal     import *
# 部品
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture

DELETE_QUERY = "DELETE FROM %s"
SELECT_QUERY = "SELECT * FROM %s"
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
        self.db = SQLCommunication()
        self.db.set_db_name(DATABESE)

    # テキストを生成
    def setting_text(self, text_index):
        if text_index in POPUP_TEXTS.keys():
            # 表示用テキストを生成
            self.view_text = self.text_font.render(POPUP_TEXTS[text_index], True, WHITE)

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

    # CSVファイルを生成
    def create_csv(self):
        with open(CSV_FILE_PATH, "w") as f:
            writer=csv.writer(f)
            for table in TARGETTABLE:
                query = SELECT_QUERY % table
                result = self.db.db_query_execution(query=query)
                writer.writerow([table + ' ----------------------------------------------------------------------'])
                for j in result:
                    j_list = list(j)
                    for k in range(len(j_list)):
                        if type(j_list[k]) is int:
                            j_list[k] = str(j_list[k])
                        elif j_list[k] is None:
                            j_list[k] = ""
                        elif type(j_list[k]) is float:
                            j_list[k] = str(j_list[k])
                    writer.writerow(list(j_list))
            

    # ボタンのイベント処理
    def yes(self):
        self.create_csv()
        for table in TARGETTABLE:
            delete_query = DELETE_QUERY % table
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