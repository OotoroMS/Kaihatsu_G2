#動作確認画面
import pygame
import sys
sys.path.append("../MAIN_DEVICE/GUI")
sys.path.append("../MAIN_DEVICE/")
from typing               import Tuple,Optional

# 定数
from GUI.constant.file_path   import *
from GUI.constant.screen_name import *
from GUI.constant.popup_name  import *
from GUI.constant.color       import *
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture
from GUI.screen.BaseScreen    import BaseScreen
# データベース接続クラス
from DATABASE.SQLCommunication import SQLCommunication

# タイトルの設定
MOTION_TETLE_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_motion.png"
}
# 各ボタンの設定
BACK_BOTTON_STATUS  = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
WASH_BOTTON_STATUS  = {
    "coordinate" : (50,  650),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_wash.png"
}
MOVE_BUTTON_STATUS  = {
    "coordinate" : (570, 170),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_move.png"
}
MEAS_BUTTON_STATUS  = {
    "coordinate" : (670, 850),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_meas.png"
}
ACCU_BUTTON_STATUS  = {
    "coordinate" : (1100,270),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_accu.png"
}
RESET_BUTTON_STATUS = {
    "coordinate" : (1570,710),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_dbreset.png"
}
PASS_BUTTON_STATUS  = {
    "coordinate" : (1570,900),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_change.png"
}
# 各種画像の設定
TARGET_EXPTXT_STATUS = {
    "coordinate" : (250, 210),
    "size"       : (1300,740),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_target.png"
}

QUERY = "DELETE FROM %s"
TARGETTABLE = [
    "db_now",
    "db_countlog",
    "db_timelog",
    "db_sizelog"
]

# 動作確認画面のメインメニュー
class MotionScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.db = SQLCommunication()
    
    # 画像の設定
    def setting_images(self):
        self.images = [
            Picture(self.screen, **MOTION_TETLE_STATUS),
            Picture(self.screen, **TARGET_EXPTXT_STATUS)
        ]
    
    # ボタンの設定
    def setting_buttons(self):
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS,  func=self.move_main),
            Button(self.screen, **WASH_BOTTON_STATUS,  func=self.move_wash),
            Button(self.screen, **MOVE_BUTTON_STATUS,  func=self.move_move),
            Button(self.screen, **MEAS_BUTTON_STATUS,  func=self.move_test03),
            Button(self.screen, **ACCU_BUTTON_STATUS,  func=self.move_test04),
            Button(self.screen, **RESET_BUTTON_STATUS, func=self.dbreset),
            Button(self.screen, **PASS_BUTTON_STATUS,  func=self.move_changepass)
        ]
    
    # 描画処理
    def draw(self):
        for image  in self.images:
            image.draw()
        pygame.draw.line(self.screen,RED,(215,680),(400,560),8)#01
        pygame.draw.line(self.screen,YELLOW,(750,260),(660,410),8)#02
        pygame.draw.line(self.screen,GREEN,(880,950),(780,670),8)#03
        pygame.draw.line(self.screen,BLUE,(1260,410),(1000,550),8)#04
        for button in self.buttons:
            button.draw()

    #   動作確認ボタン押下処理
    def move_wash(self):
        return WASH, OK
    
    def move_move(self):
        return MOVE, OK

    def move_test03(self):
        return STACK, OK
    
    def move_test04(self):
        return STACK, OK

    def dbreset(self):
        for table in TARGETTABLE:
            delete_query = QUERY % table
            print(delete_query)
            # print("変更前")
            # self.db.table_data_list_display(table_name=table)
            # self.db.db_query_execution(query=delete_query)
            # print("変更後")
            # self.db.table_data_list_display(table_name=table)
        return None, OK

    def move_changepass(self):
        return None, OK

    def move_main(self):
        return MAIN, OK
    