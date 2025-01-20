import pygame
from typing               import Tuple,Optional
# 定数
from GUI.constant.screen.change_meas_constant   import *
from GUI.constant.file_path                     import *
from GUI.constant.screen_name                   import *
from GUI.constant.popup_name                    import *
from GUI.constant.color                         import *
# 部品
from GUI.parts.Button         import Button
from GUI.parts.Picture        import Picture
# ベーススクリーン
from GUI.screen.PassScreen    import PassScreen
# データベース接続クラス
from DATABASE.SQLCommunication import SQLCommunication
UPDATE_QUERY = "UPDATE indicator set calibrate_value = "
class ChangeMeasScreen(PassScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        button = Button(self.screen, **BUTTON_DOT_STATUS, func=self.num_dot)
        button.off_hover_flag()
        self.buttons.append(button)
        self.dot_frag = True
        self.db = SQLCommunication()
        self.db.set_db_name("testdb_main.db")

    def setting_images(self):
        self.images = {
            Picture(self.screen, **TITLE_MEAS_STATUS)
        }

    def draw_pass(self):
        self.passward = self.pass_font.render(self.set_pass, True, BLACK)
        self.pass_center = self.passward.get_rect(center=self.pass_rect.center)
        pygame.draw.rect(self.screen, (255,255,255), self. pass_rect)   #   稼働状況更新の領域を確保
        pygame.draw.rect(self.screen, BLACK, self.pass_rect, 5)         #   外枠を描画
        self.screen.blit(self.passward,self.pass_center)      

    # 小数点
    def num_dot(self):
        if self.dot_frag:
            self.set_pass += "."
            self.dot_frag = False
        return None, OK

    def num_clr(self):
        self.dot_frag = True
        return super().num_clr()

    def num_check(self):
        if self.set_pass and self.set_pass[0] != ".":
            new_data = float(self.set_pass)
            self.db.db_query_execution(query=UPDATE_QUERY + str(new_data))
            return INDICATOR_OK,OK
        else:
            self.dot_frag = True
            self.set_pass = ""
        return None, OK
    
    def move_screen(self):
        self.set_pass = ""
        return MEAS, OK