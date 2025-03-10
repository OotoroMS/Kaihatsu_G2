#良否カウントログ画面
import pygame
import CountList
import DrawTable
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
FONT = "C:\\Windows\\Fonts\\msgothic.ttc"

class CountFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.table_font = pygame.font.Font(FONT,size=110)
        self.bad_view = 0
        self.bad_cnt = 0
        self.view = "today"
        self.scrol = False
        self.setting_buttons() 
    
    def setting_buttons(self):
        self.buttons = {
            Button(self.screen, 20, 280, 360, 140, "GUI_option_test\\image\\button\\pic11.png", self.move_today),#当日
            Button(self.screen, 20, 470, 360, 140, "GUI_option_test\\image\\button\\pic09.png", self.move_seven),#七日間
            Button(self.screen, 20, 660, 360, 140, "GUI_option_test\\image\\button\\pic10.png", self.move_error),#不良発生時間
            Button(self.screen, 0, 960, 330, 120, "GUI_option_test\\image\\button\\back.png", self.move_data)
        }
        self.scrol_buttons = {
            Button(self.screen, 1570, 280, 220, 160, "GUI_option_test\\image\\button\\pic14.png", self.table_full_up),#一番上
            Button(self.screen, 1590, 480, 180, 120, "GUI_option_test\\image\\button\\pic15.png", self.table_up),#上
            Button(self.screen, 1590, 640, 180, 120, "GUI_option_test\\image\\button\\pic16.png", self.table_down),#下
            Button(self.screen, 1570, 810, 220, 160, "GUI_option_test\\image\\button\\pic17.png", self.table_full_down)#一番下
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, "GUI_option_test\\image\\title\\pic07.png")#良否カウントログ
        }

    #   画面描画処理
    def draw(self):
        for image in self.images:
            image.draw()
        self.draw_buttons()
        self.bad_cnt = DrawTable.draw_table(self.screen, self.view, self.bad_view, self.table_font)
        # if self.view == "error":
        #     print("bad_cnt :",self.bad_cnt)
    
    #   イベント処理を記述
    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    move = button.is_clicked(event)
                    if move:
                        break
                for button in self.scrol_buttons:
                    button.is_clicked(event)
                return move

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()
        if self.scrol:
            for button in self.scrol_buttons:
                button.draw()

    #  当日
    def move_today(self):
        self.view = "today"
        self.scrol = False
        self.table_font = pygame.font.Font(FONT,size=110)
    #七日間
    def move_seven(self):
        self.view = "seven"
        self.scrol = False
        self.table_font = pygame.font.Font(FONT,size=50)
    #不良発生時間
    def move_error(self):
        self.bad_view = 0
        self.scrol = True
        self.view = "error"
        self.table_font = pygame.font.Font(FONT,size=50)
    #上
    def table_up(self):
        if self.bad_view > 0:
            self.bad_view -= 2*5
        if self.bad_view < 0:
            self.bad_view = 0
        print("self.bad_view :", self.bad_view)
    #一番上
    def table_full_up(self):
        if self.bad_view > 0:
            self.bad_view = 0
        print("self.bad_view :", self.bad_view)
    #下
    def table_down(self):
        if self.bad_cnt > 14:
            if self.bad_view < self.bad_cnt - 14:
                self.bad_view += 2*5
            if self.bad_view > self.bad_cnt - 14:
                self.bad_view = self.bad_cnt - 14
            print("self.bad_view :", self.bad_view)
    #一番下
    def table_full_down(self):
        if self.bad_view < self.bad_cnt - 14:
            self.bad_view = self.bad_cnt - 14
        print("self.bad_view :", self.bad_view)

    #   データ一覧画面に遷移
    def move_data(self):
        self.scrol = False
        self.view = "today"
        return "data"