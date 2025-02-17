#パスワード入力画面
import pygame
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from parts.SQLCommunication_main import SQLCommunication
from filepath import *

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
POPUPMSSEGE = "パスワードが違います" 
PASSINPUTMAX = 11
DBNAME = "testdb_main.db"
QUERY = "select num from pass_num"
#   メイン画面描画・処理クラス
class PassFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.pass_font = pygame.font.Font(font, 80)
        self.pass_rect = pygame.rect.Rect(660, 200, 600, 170)
        self.set_pass = ""
        self.flg_veiw_popup = False
        self.buttons = [
            Button(self.screen, 0,    960, 330, 120, IMAGEFILEPATH + "button\\back.png",  self.move_main),
            Button(self.screen, 660,  915, 370, 200, IMAGEFILEPATH + "button\\pic20.png", self.num_0),
            Button(self.screen, 660,  750, 180, 180, IMAGEFILEPATH + "button\\pic21.png", self.num_1),
            Button(self.screen, 850,  750, 180, 180, IMAGEFILEPATH + "button\\pic22.png", self.num_2),
            Button(self.screen, 1040, 750, 180, 180, IMAGEFILEPATH + "button\\pic23.png", self.num_3),
            Button(self.screen, 660,  570, 180, 180, IMAGEFILEPATH + "button\\pic24.png", self.num_4),
            Button(self.screen, 850,  570, 180, 180, IMAGEFILEPATH + "button\\pic25.png", self.num_5),
            Button(self.screen, 1040, 570, 180, 180, IMAGEFILEPATH + "button\\pic26.png", self.num_6),
            Button(self.screen, 660,  390, 180, 180, IMAGEFILEPATH + "button\\pic27.png", self.num_7),
            Button(self.screen, 850,  390, 180, 180, IMAGEFILEPATH + "button\\pic28.png", self.num_8),
            Button(self.screen, 1040, 390, 180, 180, IMAGEFILEPATH + "button\\pic29.png", self.num_9),
            Button(self.screen, 1230, 390, 175, 173, IMAGEFILEPATH + "button\\pic30.png", self.num_clr),
            Button(self.screen, 1211, 570, 212, 360, IMAGEFILEPATH + "button\\pic31.png", self.num_check)
        ]
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, IMAGEFILEPATH + "title\\pic71.png"),
            Picture(self.screen, 410, 200, 180, 180, IMAGEFILEPATH + "button\\pic19.png")
        }
        self.db = SQLCommunication()
        self.db.set_db_name(DBNAME)
    
    #   ボタン及びテキストの描画処理を記述
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

    def move_main(self):
        self.set_pass = ""
        return "main"
    
    def num_0(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "0"
    def num_1(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "1"
    def num_2(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "2"
    def num_3(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "3"
    def num_4(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "4"
    def num_5(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "5"
    def num_6(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "6"
    def num_7(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "7"
    def num_8(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "8"
    def num_9(self):
        if len(self.set_pass) <= PASSINPUTMAX:
            self.set_pass += "9"
    
    def num_clr(self):
        self.set_pass = ""
    
    def num_check(self):
        password = self.db.db_query_execution(query=QUERY)
        print(password[0])
        if self.set_pass == password[0][0]:
            self.set_pass = ""
            return "motiontest"
        else:
            self.set_pass = ""
            return "not_pass"