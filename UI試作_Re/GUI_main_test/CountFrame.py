
import pygame
import CountList
import DrawTable
from BaseFrame import BaseFrame
from Button import Button
from NumButton import NumButton

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
FONT = "C:\\Windows\\Fonts\\msgothic.ttc"

class CountFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.text_title = self.font_title.render("寸法検査ログ", True, BLACK)
        self.table_font = pygame.font.Font(FONT,size=110)
        self.bad_view = 0
        self.bad_cnt = 0
        self.view = "today"
        self.scrol = False
        self.setting_buttons() 
    
    def setting_buttons(self):
        self.buttons = {
            NumButton(self.screen, 50, 100, 220, 100, GRAY, "本日", 50, self.move_today),
            NumButton(self.screen, 50, 250, 220, 100, GRAY, "七日間", 50, self.move_seven),
            NumButton(self.screen, 50, 400, 220, 100, GRAY, "不良一覧", 50, self.move_error),
            Button(self.screen, 1570, 930, 330, 120, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\return.png", self.move_data)
        }
        self.scrol_buttons = {
            NumButton(self.screen, 1450, 435, 220, 100, GRAY, "　△　", 50, self.table_up),
            NumButton(self.screen, 1450, 545, 220, 100, GRAY, "　▽　", 50, self.table_down),
            NumButton(self.screen, 1450, 380, 220, 50, GRAY, "△△△", 50, self.table_full_up),
            NumButton(self.screen, 1450, 650, 220, 50, GRAY, "▽▽▽", 50, self.table_full_down)
        }

    #   画面描画処理
    def draw(self):
        self.screen.blit(self.text_title,(200,10))
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