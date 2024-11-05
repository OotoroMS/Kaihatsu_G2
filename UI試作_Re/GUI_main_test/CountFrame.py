#良否カウントログ
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
            Button(self.screen, 20, 280, 360, 140, "GUI_main_test\\image\\button\\pic11.png", self.move_today),#当日
            Button(self.screen, 20, 470, 360, 140, "GUI_main_test\\image\\button\\pic09.png", self.move_seven),#7
            Button(self.screen, 20, 660, 360, 140, "GUI_main_test\\image\\button\\pic10.png", self.move_error),#不良
            Button(self.screen, 0, 960, 330, 120, "GUI_main_test\\image\\button\\back.png", self.move_data)
        }
        self.scrol_buttons = {
            Button(self.screen, 1570, 280, 220, 160, "GUI_main_test\\image\\button\\pic14.png", self.table_full_up),
            Button(self.screen, 1590, 480, 180, 120, "GUI_main_test\\image\\button\\pic15.png", self.table_up),
            Button(self.screen, 1590, 640, 180, 120, "GUI_main_test\\image\\button\\pic16.png", self.table_down),
            Button(self.screen, 1570, 810, 220, 160, "GUI_main_test\\image\\button\\pic17.png", self.table_full_down)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, "GUI_main_test\\image\\title\\pic07.png")
        }

    #   画面描画処理
    def draw(self):
        for image in self.images:
            image.draw()
        self.draw_buttons()
        DrawTable.draw_table(self.screen, self.view, self.bad_view, self.table_font)

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()
        if self.scrol:
            for button in self.scrol_buttons:
                button.draw()

    #   良否カウント画面に遷移
    def move_today(self):
        self.view = "today"
        self.scrol = False
        self.table_font = pygame.font.Font(FONT,size=110)

    def move_seven(self):
        self.view = "seven"
        self.scrol = False
        self.table_font = pygame.font.Font(FONT,size=50)
    
    def move_error(self):
        self.bad_view = 0
        self.scrol = True
        self.view = "error"
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