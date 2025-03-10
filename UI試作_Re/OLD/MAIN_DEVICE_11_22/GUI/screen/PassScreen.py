#パスワード画面
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

PASSINPUTMAX   = 11
PASS_FONT_SIZE = 80
NUM_BUTTONS_X = [660, 850, 1040]
NUM_BUTTONS_Y = [750, 570, 390]
NUM_BUTTONS_SIZE = (180,180)
NUM_BUTTONS_FILE_PATH = [
    BUTTON_FILE_PATH + "button_1.png",
    BUTTON_FILE_PATH + "button_2.png",
    BUTTON_FILE_PATH + "button_3.png",
    BUTTON_FILE_PATH + "button_4.png",
    BUTTON_FILE_PATH + "button_5.png",
    BUTTON_FILE_PATH + "button_6.png",
    BUTTON_FILE_PATH + "button_7.png",
    BUTTON_FILE_PATH + "button_8.png",
    BUTTON_FILE_PATH + "button_9.png",
]

PASS_TITLE_STATUS  = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_pass.png"
}
BACK_BOTTON_STATUS = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
ZERO_BUTON_STATUS  = {
    "coordinate" : (660, 915),
    "size"       : (370, 200),
    "image_path" : BUTTON_FILE_PATH + "button_0.png"
}
CLR_BUTTON_STATUS  = {
    "coordinate" : (1230,390),
    "size"       : (175, 173),
    "image_path" : BUTTON_FILE_PATH + "button_clr.png"
}
ENT_BUTTON_STATUS  = {
    "coordinate" : (1211,570),
    "size"       : (212, 360),
    "image_path" : BUTTON_FILE_PATH + "button_ent.png"
}
ROCK_EXPEXT_STATUS = {
    "coordinate" : (410, 200),
    "size"       : (180, 180),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_rock.png"
}

QUERY        = "select num from pass_num"


class PassScreen(BaseScreen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.set_pass = ""
        self.db = SQLCommunication()
        self.pass_font = pygame.font.Font(FONT, PASS_FONT_SIZE)
        self.pass_rect = pygame.rect.Rect(660, 200, 600, 170)
    
    def create_func_list(self):
        self.func_list = [
            self.num_1,
            self.num_2,
            self.num_3,
            self.num_4,
            self.num_5,
            self.num_6,
            self.num_7,
            self.num_8,
            self.num_9
        ]

    def setting_buttons(self):
        self.create_func_list()
        self.buttons = [
            Button(self.screen, **BACK_BOTTON_STATUS, func=self.move_main),
            Button(self.screen, **CLR_BUTTON_STATUS,  func=self.num_clr),
            Button(self.screen, **ENT_BUTTON_STATUS,  func=self.num_check),
            Button(self.screen, **ZERO_BUTON_STATUS,  func=self.num_0)
        ]
        self.buttons[3].off_hover_flag()
        func_index = 0
        for y in range(0,3):
            for x in range(0,3):
                button = Button(self.screen, (NUM_BUTTONS_X[x], NUM_BUTTONS_Y[y]), NUM_BUTTONS_SIZE,NUM_BUTTONS_FILE_PATH[func_index], self.func_list[func_index])
                button.off_hover_flag()
                self.buttons.append(button)
                func_index += 1
        

    def setting_images(self):
        self.images = [
            Picture(self.screen, **PASS_TITLE_STATUS),
            Picture(self.screen, **ROCK_EXPEXT_STATUS)
        ]

    def draw(self):
        for image in self.images:
            image.draw()
        self.draw_pass()
        for button in self.buttons:
            button.draw()

    def draw_pass(self):
        self.passward = self.pass_font.render(self.set_pass, True, BLACK)
        self.pass_center = self.passward.get_rect(center=self.pass_rect.center)
        pygame.draw.rect(self.screen, (255,255,255), self. pass_rect)   #   稼働状況更新の領域を確保
        pygame.draw.rect(self.screen, BLACK, self.pass_rect, 5)         #   外枠を描画
        self.screen.blit(self.passward,self.pass_center)


    def num_0(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "0"
        return None, OK
    def num_1(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "1"
        return None, OK
    def num_2(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "2"
        return None, OK
    def num_3(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "3"
        return None, OK
    def num_4(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "4"
        return None, OK
    def num_5(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "5"
        return None, OK
    def num_6(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "6"
        return None, OK
    def num_7(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "7"
        return None, OK
    def num_8(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "8"
        return None, OK
    def num_9(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "9"
        return None, OK
    
    def num_clr(self):
        self.set_pass = ""
        return None, OK
    
    def num_check(self):
        query_resurt = self.db.db_query_execution(DATABESE,query=QUERY)
        if query_resurt:
            password = query_resurt[0][0]
        else:
            password = "2024"
        if self.set_pass == password:
            self.set_pass = ""
            return MOTION , OK 
        else:
            self.set_pass = ""
            return None, OK
    
    def move_main(self):
        return MAIN, OK