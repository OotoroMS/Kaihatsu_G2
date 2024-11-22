#良否カウントログ
import pygame
import sys
sys.path.append("../MAIN_DEVICE/GUI")
sys.path.append("../MAIN_DEVICE/")
from typing               import Tuple,Optional
# 自作モジュール
import GUI.parts.DrawTable    as DrawTable
# 定数
from GUI.constant.file_path   import *
from GUI.constant.screen_name import *
from GUI.constant.popup_name  import *
# 部品
from GUI.parts.Button         import Button, SIZE_SCALE, CORDINATE_SCALE
from GUI.parts.Picture        import Picture
# 継承元クラス
from GUI.screen.BaseScreen    import BaseScreen
# データベース接続クラス
from DATABASE.SQLCommunication import SQLCommunication
# CORDINATEのindex
X      = 0
Y      = 1
# SIZEのindex
WIDTH  = 0
HEIGHT = 1
# スクロール機能のON/OFF
ON  = True
OFF = False
# 表示内容
TODAY = "today"
SEVEN = "seven"
ERROR = "error"
# 表のフォントサイズ
FONT_SIZE = {
    TODAY : 110,
    SEVEN : 50,
    ERROR : 50
}
# 各選択ボタンの座標
CORDINATE_TODAY = (20, 280)
CORDINATE_SEVEN = (20, 470)
CORDINATE_ERROR = (20, 660)
# 各選択ボタンのwhidth, height
SIZE_SELECT_BUTTON = (360, 140)
SIZE_SELECT_IMAGE  = (SIZE_SELECT_BUTTON[WIDTH] * SIZE_SCALE, SIZE_SELECT_BUTTON[HEIGHT] * SIZE_SCALE)
# 戻るボタンの設定
BUTTON_BACK_STATUS  = {
    "coordinate" : (0,   960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
# 閲覧記録切替ボタンの設定
BUTTON_TODAY_STATUS = {
    "coordinate" : CORDINATE_TODAY,
    "size"       : SIZE_SELECT_BUTTON,
    "image_path" : BUTTON_FILE_PATH + "button_today.png"
}
BUTTON_SEVEN_STATUS = {
    "coordinate" : CORDINATE_SEVEN,
    "size"       : SIZE_SELECT_BUTTON,
    "image_path" : BUTTON_FILE_PATH + "button_seven.png"
}
BUTTON_ERROR_STATUS = {
    "coordinate" : CORDINATE_ERROR,
    "size"       : SIZE_SELECT_BUTTON,
    "image_path" : BUTTON_FILE_PATH + "button_error.png"
}
# スクロールボタンの設定
BUTTON_FULLUP_SCROL_STATUS   = {
    "coordinate" : (1570,280),
    "size"       : (220, 160),
    "image_path" : BUTTON_FILE_PATH + "button_fullup.png"
}
BUTTON_UP_SCROL_STATUS       = {
    "coordinate" : (1590,480),
    "size"       : (180, 130),
    "image_path" : BUTTON_FILE_PATH + "button_up.png"
}
BUTTON_DOWN_SCROL_STATUS     = {
    "coordinate" : (1590,640),
    "size"       : (180, 130),
    "image_path" : BUTTON_FILE_PATH + "button_down.png"
}
BUTTON_FULLDOWN_SCROL_STATUS = {
    "coordinate" : (1570,810),
    "size"       : (220, 160),
    "image_path" : BUTTON_FILE_PATH + "button_fulldown.png"
}
# 現在の表示内容の設定
IMAGE_TODAY_STATUS  = {
    "coordinate" : (CORDINATE_TODAY[X]  - (SIZE_SELECT_BUTTON[WIDTH] * CORDINATE_SCALE) // 2, CORDINATE_TODAY[Y] - (SIZE_SELECT_BUTTON[HEIGHT] * CORDINATE_SCALE) // 2),
    "size"       : SIZE_SELECT_IMAGE,
    "image_path" : EXPTXT_FILE_PATH + "exptxt_today.png"
}
IMAGE_SEVEN_STATUS  = {
    "coordinate" : (CORDINATE_SEVEN[X]  - (SIZE_SELECT_BUTTON[WIDTH] * CORDINATE_SCALE) // 2, CORDINATE_SEVEN[Y] - (SIZE_SELECT_BUTTON[HEIGHT] * CORDINATE_SCALE) // 2),
    "size"       : SIZE_SELECT_IMAGE,
    "image_path" : EXPTXT_FILE_PATH + "exptxt_seven.png"
}
IMAGE_ERROR_STATUS  = {
    "coordinate" : (CORDINATE_ERROR[X]  - (SIZE_SELECT_BUTTON[WIDTH] * CORDINATE_SCALE) // 2, CORDINATE_ERROR[Y] - (SIZE_SELECT_BUTTON[HEIGHT] * CORDINATE_SCALE) // 2),
    "size"       : SIZE_SELECT_IMAGE,
    "image_path" : EXPTXT_FILE_PATH + "exptxt_error.png"
}
# タイトル
COUNT_TITLE_STAUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_count.png"
}
# データ確認用QUERY
QUERY = {
    SEVEN : "select * from db_countlog order by id DESC limit 7",
    ERROR : "select * from db_timelog order by id DESC limit 50"
}
class CountScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.font  = pygame.font.Font(FONT, size=FONT_SIZE[TODAY])
        self.view  = TODAY
        self.scrol = OFF

        self.bad_index = 0     # 不良発生データの表示開始インデックス
        self.bad_count = None  # 不良発生データの総数(error時のみデータを代入)
        self.db = SQLCommunication()

    # 表示画像設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **COUNT_TITLE_STAUS)
        ]
        self.select_images = {
            TODAY : Picture(self.screen, **IMAGE_TODAY_STATUS),
            SEVEN : Picture(self.screen, **IMAGE_SEVEN_STATUS),
            ERROR : Picture(self.screen, **IMAGE_ERROR_STATUS)
        }
    
    # 表示ボタン設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BUTTON_BACK_STATUS, func=self.move_data)
        ]
        # 各選択ボタン
        self.select_buttons = {
            TODAY : Button(self.screen, **BUTTON_TODAY_STATUS, func = self.change_display_today),
            SEVEN : Button(self.screen, **BUTTON_SEVEN_STATUS, func = self.change_display_seben),
            ERROR : Button(self.screen, **BUTTON_ERROR_STATUS, func = self.change_display_error)
        }
        # スクロールボタン
        self.scrol_buttons = [
            Button(self.screen, **BUTTON_FULLUP_SCROL_STATUS,   func = self.table_list_fullup),
            Button(self.screen, **BUTTON_UP_SCROL_STATUS,       func = self.table_list_up),
            Button(self.screen, **BUTTON_DOWN_SCROL_STATUS,     func = self.table_list_down),
            Button(self.screen, **BUTTON_FULLDOWN_SCROL_STATUS, func = self.table_list_fulldown)
        ]
    
    # 描画処理
    def draw(self):
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        self.draw_buttons()
        self.font = pygame.font.Font(FONT, size=FONT_SIZE[self.view])
        self.bad_count = DrawTable.draw_table(self.screen, self.view, self.bad_index, self.font)
    
    # 各選択ボタンとスクロールボタンの描画処理
    def draw_buttons(self):
        for key in self.select_buttons:
            if key == self.view:
                self.select_images[key].draw()
            else:
                self.select_buttons[key].draw()

        if self.scrol:
            for button in self.scrol_buttons:
                button.draw()

    # 押下処理
    def clicked(self, event):
        result = ""
        normal = False
        # ボタンに位置でクリック(タップ)されていたら紐づけられた処理を行う
        for button in self.buttons:
            result,normal = button.is_clicked(event)
            if normal:
                return result, normal
        for key in self.select_buttons:
            if key != self.view:
                result,normal = self.select_buttons[key].is_clicked(event)
                if normal:
                    return result, normal
        if self.scrol:
            for button in self.scrol_buttons:
                result,normal = button.is_clicked(event)
                if normal:
                    return result,normal
        return result, normal
    
    # 当日の記録
    def change_display_today(self):
        self.view  = TODAY
        self.scrol = False
        return None, OK
    
    # 七日間の記録
    def change_display_seben(self):
        result = self.db.db_query_execution(DATABESE,QUERY[SEVEN])
        if result:
            self.view  = SEVEN
            self.scrol = False
            return None, OK
        return None, NG
    
    # 不良発生時刻の記録
    def change_display_error(self):
        result = self.db.db_query_execution(DATABESE,QUERY[ERROR])
        if result:
            self.view = ERROR
            self.scrol = ON
            self.bad_index = 0
            return None, OK
        return None, NG

    # 表の表示を一番上へ移動
    def table_list_fullup(self):
        if self.bad_index > 0:
            self.bad_index = 0
            return None, OK
        return None, False
    
    # 表の表示を1行上へ移動
    def table_list_up(self):
        if self.bad_index > 0:
            self.bad_index -= 2*5
        if self.bad_index < 0:
            self.bad_index = 0
        return None, OK
    
    # 表の表示を1行下へ移動
    def table_list_down(self):
        if self.bad_count > 14:
            if self.bad_index < self.bad_count - 14:
                self.bad_index += 2*5
            if self.bad_index > self.bad_count - 14:
                self.bad_index = self.bad_count - 14
        return None, True

    # 表の表示を一番下へ移動
    def table_list_fulldown(self):
        if self.bad_index < self.bad_count - 14:
            self.bad_index = self.bad_count - 14
        return None, True
    
    # データ一覧画面へ移動
    def move_data(self):
        self.scrol = OFF
        self.view  = TODAY
        return DATA, OK
