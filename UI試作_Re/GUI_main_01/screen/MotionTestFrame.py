#動作確認画面
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from parts.SQLCommunication_main import SQLCommunication
from filepath import *
import pygame

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
RED  = ((255,0,0))#RGB
GREEN  = ((0,255,0))
BLUE  = ((0,0,255))
YELLOW  = ((255,255,0))
MAINTITLE=IMAGEFILEPATH + "title\\pic62.png"

DBNAME = "testdb_main.db" 
QUERY = "DELETE FROM %s"
TARGETTABLE = [
    "db_now",
    "db_countlog",
    "db_timelog",
    "db_sizelog"
]

#   メイン画面描画・処理クラス
class MotionTestFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 50,   650, 330, 150, IMAGEFILEPATH + "button\\pic33.png", self.move_test01),
            Button(self.screen, 570,  170, 330, 150, IMAGEFILEPATH + "button\\pic34.png", self.move_test02),
            Button(self.screen, 670,  850, 330, 150, IMAGEFILEPATH + "button\\pic35.png", self.move_test03),
            Button(self.screen, 1100, 270, 330, 150, IMAGEFILEPATH + "button\\pic36.png", self.move_test04),
            Button(self.screen, 1570, 710, 330, 150, IMAGEFILEPATH + "button\\pic74.png", self.dbreset),
            Button(self.screen, 1570, 900, 330, 150, IMAGEFILEPATH + "button\\pic37.png", self.move_changepass),
            Button(self.screen, 0,    960, 330, 120, IMAGEFILEPATH + "button\\back.png",  self.move_main)
        }
        self.images = {
            Picture(self.screen, 0,   0,   750,  200, MAINTITLE),
            Picture(self.screen, 250, 210, 1300, 740, IMAGEFILEPATH + "exptxt\\pic32.png")
        }
        self.db = SQLCommunication()
        self.db.set_db_name(DBNAME)

    def draw(self):
        for image in self.images:
            image.draw()
        pygame.draw.line(self.screen,RED,(215,680),(400,560),8)#01
        pygame.draw.line(self.screen,YELLOW,(750,260),(660,410),8)#02
        pygame.draw.line(self.screen,GREEN,(880,950),(780,670),8)#03
        pygame.draw.line(self.screen,BLUE,(1260,410),(1000,550),8)#04
        for button in self.buttons:
            button.draw()

    #   動作確認ボタン押下処理
    def move_test01(self):
        return "test01"
    
    def move_test02(self):
        return "test02"

    def move_test03(self):
        return "test03"
    
    def move_test04(self):
        return "test04"

    def dbreset(self):
        return "db_reset"


    def move_changepass(self):
        return "changepass"

    def move_main(self):
        return "main"