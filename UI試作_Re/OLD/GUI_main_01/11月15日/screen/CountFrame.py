#良否カウントログ
import pygame

import count.CountList as CountList
import count.DrawTable as DrawTable
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from parts.SQLCommunication_main import SQLCommunication
from filepath import *

DBNAME =  "testdb_main.db"

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
FONT  = "C:\\Windows\\Fonts\\msgothic.ttc"
TODAY = "today"
SEVEN = "seven"
ERROR = "error"
QUERY = {
    "seven" : "select * from db_countlog order by id DESC limit 7",
    "error" : "select * from db_timelog order by id DESC limit 50"
}


class CountFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.db = SQLCommunication()
        self.table_font = pygame.font.Font(FONT,size=110)
        self.bad_view = 0
        self.bad_cnt = 0
        self.view = "today"
        self.scrol = False
        self.setting_buttons()
        self.select_images = {
            TODAY : Picture(self.screen, 20 - (360 * (1.1 - 1)) // 2, 280 - (140 * (1.1 - 1)) // 2, 360*1.1, 140*1.1, IMAGEFILEPATH + "button\\pic08.png"),
            SEVEN : Picture(self.screen, 20 - (360 * (1.1 - 1)) // 2, 470 - (140 * (1.1 - 1)) // 2, 360*1.1, 140*1.1, IMAGEFILEPATH + "button\\pic12.png"),
            ERROR : Picture(self.screen, 20 - (360 * (1.1 - 1)) // 2, 660 - (140 * (1.1 - 1)) // 2, 360*1.1, 140*1.1, IMAGEFILEPATH + "button\\pic13.png")
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, IMAGEFILEPATH + "title\\pic07.png")
        }
    
    def setting_buttons(self):
        self.buttons = {
            Button(self.screen, 0, 960, 330, 120,  IMAGEFILEPATH + "button\\back.png", self.move_data)
        }
        self.select_buttons={
            TODAY:Button(self.screen, 20, 280, 360, 140, IMAGEFILEPATH + "button\\pic11.png", self.move_today),#当日
            SEVEN:Button(self.screen, 20, 470, 360, 140, IMAGEFILEPATH + "button\\pic09.png", self.move_seven),#7
            ERROR:Button(self.screen, 20, 660, 360, 140, IMAGEFILEPATH + "button\\pic10.png", self.move_error),#不良
        }
        self.scrol_buttons = {
            Button(self.screen, 1570, 280, 220, 160, IMAGEFILEPATH + "button\\pic14.png", self.table_full_up),
            Button(self.screen, 1590, 480, 180, 120, IMAGEFILEPATH + "button\\pic15.png", self.table_up),
            Button(self.screen, 1590, 640, 180, 120, IMAGEFILEPATH + "button\\pic16.png", self.table_down),
            Button(self.screen, 1570, 810, 220, 160, IMAGEFILEPATH + "button\\pic17.png", self.table_full_down)
        }


    #   画面描画処理
    def draw(self):
        for image in self.images:
            image.draw()
        self.draw_buttons()
        self.bad_cnt = DrawTable.draw_table(self.screen, self.view, self.bad_view, self.table_font)

        #   イベント処理を記述
    def update(self):
        reaction = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                reaction = self.there_is_a_click_event(event)
        return reaction
    # def update(self):
    #     move = None
    #     for event in pygame.event.get():
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             for button in self.buttons:
    #                 move = button.is_clicked(event)
    #                 if move:
    #                     break
    #             for button in self.scrol_buttons:
    #                 button.is_clicked(event)
    #             return move
            
    def there_is_a_click_event(self, event : pygame.event.Event):
        reaction = None
        for button in self.buttons:
            reaction = button.is_clicked(event)
            if reaction:
                return reaction
        for key in self.select_buttons:
            if key != self.view:
                reaction = self.select_buttons[key].is_clicked(event)
            if reaction:
                return reaction
        for button in self.scrol_buttons:
            button.is_clicked(event)
        return reaction

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()
        for key    in self.select_buttons:
            if key == self.view:
                self.select_images[key].draw()
            else:
                self.select_buttons[key].draw()
        if self.scrol:
            for button in self.scrol_buttons:
                button.draw()

    #   当日
    def move_today(self):
        self.view = "today"
        self.scrol = False
        self.table_font = pygame.font.Font(FONT,size=110)
    #七日間
    def move_seven(self):
        if self.db_data_check("seven"):
            self.view = "seven"
        else:
            return "none_data"
        self.scrol = False
        self.table_font = pygame.font.Font(FONT,size=50)
    #不良発生時間 
    def move_error(self):
        if self.db_data_check("seven"):
            self.bad_view = 0
            self.scrol = True
            self.view = "error"
        else:
            return "none_data"
        self.table_font = pygame.font.Font(FONT,size=50)

    def table_up(self):
        if self.bad_view > 0:
            self.bad_view -= 2*5
        if self.bad_view < 0:
            self.bad_view = 0
    
    def table_full_up(self):
        if self.bad_view > 0:
            self.bad_view = 0

    def table_down(self):
        if self.bad_cnt > 14:
            if self.bad_view < self.bad_cnt - 14:
                self.bad_view += 2*5
            if self.bad_view > self.bad_cnt - 14:
                self.bad_view = self.bad_cnt - 14
            
    def table_full_down(self):
        if self.bad_view < self.bad_cnt - 14:
            self.bad_view = self.bad_cnt - 14

    #   データ一覧画面に遷移
    def move_data(self):
        self.scrol = False
        self.view = "today"
        return "data"
    
    def db_data_check(self, view):
        result = self.db.db_query_execution(DBNAME, QUERY[view])
        if result:
            return True
        return False
