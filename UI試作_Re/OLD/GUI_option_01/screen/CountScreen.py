#良否カウントログ画面
import pygame

# 定数
from constant.FilePath   import *
from constant.ScreenName import *
from constant.PopupName  import *
# モジュール
import parts.CountList as CountList
import parts.DrawTable as DrawTable
from DB.SQLCommunication import SQLCommunication
# 画面クラス
from screen.BaseScreen   import BaseFrame
# 部品クラス
from parts.Button        import Button
from parts.Picture       import Picture

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
FONT = "C:\\Windows\\Fonts\\msgothic.ttc"
DATABESE = "testdb_option.db"
TODAY = "today"
SEVEN = "seven"
ERROR = "error"
QUERY = {
    SEVEN : "select * from db_countlog order by id DESC limit 7",
    ERROR : "select * from db_timelog order by id DESC limit 50"
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
            TODAY : Picture(self.screen, 20 - (360 * (1.1 - 1)) // 2, 280 - (140 * (1.1 - 1)) // 2, 360*1.1, 140*1.1, BUTTONFILEPATH + "pic08.png"),
            SEVEN : Picture(self.screen, 20 - (360 * (1.1 - 1)) // 2, 470 - (140 * (1.1 - 1)) // 2, 360*1.1, 140*1.1, BUTTONFILEPATH + "pic12.png"),
            ERROR : Picture(self.screen, 20 - (360 * (1.1 - 1)) // 2, 660 - (140 * (1.1 - 1)) // 2, 360*1.1, 140*1.1, BUTTONFILEPATH + "pic13.png")
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, TITLEFILEPATH  + "pic07.png")#良否カウントログ
        }
    
    def setting_buttons(self):
        self.buttons = {
            Button(self.screen, 0,  960, 330, 120, BUTTONFILEPATH + "back.png", self.move_data)
        }
        self.select_buutons = {
            TODAY : Button(self.screen, 20, 280, 360, 140, BUTTONFILEPATH + "pic11.png", self.move_today),#当日
            SEVEN : Button(self.screen, 20, 470, 360, 140, BUTTONFILEPATH + "pic09.png", self.move_seven),#七日間
            ERROR : Button(self.screen, 20, 660, 360, 140, BUTTONFILEPATH + "pic10.png", self.move_error),#不良発生時間)
        }
        self.scrol_buttons = {
            Button(self.screen, 1570, 280, 220, 160, BUTTONFILEPATH + "pic14.png", self.table_full_up),#一番上
            Button(self.screen, 1590, 480, 180, 120, BUTTONFILEPATH + "pic15.png", self.table_up),#上
            Button(self.screen, 1590, 640, 180, 120, BUTTONFILEPATH + "pic16.png", self.table_down),#下
            Button(self.screen, 1570, 810, 220, 160, BUTTONFILEPATH + "pic17.png", self.table_full_down)#一番下
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
        for key in self.select_buutons:
            if key != self.view:
                reaction = self.select_buutons[key].is_clicked(event)
            if reaction:
                return reaction
        for button in self.scrol_buttons:
            button.is_clicked(event)
        return reaction

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()
        for key    in self.select_buutons:
            if key == self.view:
                self.select_images[key].draw()
            else:
                self.select_buutons[key].draw()

        if self.scrol:
            for button in self.scrol_buttons:
                button.draw()
    
    # def draw_buttons(self):
    #     for button in self.buttons:
    #         button.draw()
    #     if self.scrol:
    #         for button in self.scrol_buttons:
    #             button.draw()

    #  当日
    def move_today(self):
        self.view = TODAY
        self.scrol = False
        self.table_font = pygame.font.Font(FONT,size=110)
    #七日間
    def move_seven(self):
        result = self.db.db_query_execution(DATABESE, QUERY[SEVEN])
        if result:
            self.view = SEVEN
            self.scrol = False
            self.table_font = pygame.font.Font(FONT,size=50)
        else:
            return NO_DATA
    #不良発生時間
    def move_error(self):
        result = self.db.db_query_execution(DATABESE, QUERY[ERROR])
        if result:
            self.bad_view = 0
            self.scrol = True
            self.view = ERROR
            self.table_font = pygame.font.Font(FONT,size=50)
        else:
            return NO_DATA
    #上
    def table_up(self):
        if self.bad_view > 0:
            self.bad_view -= 2*5
        if self.bad_view < 0:
            self.bad_view = 0

    #一番上
    def table_full_up(self):
        if self.bad_view > 0:
            self.bad_view = 0

    #下
    def table_down(self):
        if self.bad_cnt > 14:
            if self.bad_view < self.bad_cnt - 14:
                self.bad_view += 2*5
            if self.bad_view > self.bad_cnt - 14:
                self.bad_view = self.bad_cnt - 14

    #一番下
    def table_full_down(self):
        if self.bad_view < self.bad_cnt - 14:
            self.bad_view = self.bad_cnt - 14

    #   データ一覧画面に遷移
    def move_data(self):
        self.scrol = False
        self.view = "today"
        return DATA