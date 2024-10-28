import pygame
from pygame.locals import *
import CountList
from BaseFrame import BaseFrame
from Button import Button


BRACK = ((0,0,0))
WHITE = ((255,255,255))

TODAY = ["日付", "総個数", "良品", "不良品"]
SEVEN = ["日付", "総個数", "良品", "不良品"]
ERROR = ["番号", "日付"]

#   データ一覧
class CountFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen)
        self.font = pygame.font.Font(font, 60)
        self.table_font = pygame.font.Font("C:\\Windows\\Fonts\\msgothic.ttc",size=110)
        self.title_text = self.font.render("良否カウント", True, BRACK)
        #   ボタンクラス
        self.buttons = {
            0   : Button(self.screen, 50, 100, 220, 100, WHITE, "本日", 50, self.move_today),
            1   : Button(self.screen, 50, 250, 220, 100, WHITE, "七日間", 50, self.move_seven),
            2   : Button(self.screen, 50, 450, 220, 100, WHITE, "不良一覧", 50, self.move_error),
            3   : Button(self.screen, 1570, 930, 300, 100, WHITE, "戻る", 90, self.move_main)
        }
        #   表示内容
        self.view = "today"
        #   不良表示用
        self.bad_buttons = {
            0   : Button(self.screen, 1450, 435, 220, 100, WHITE, "　△　", 50, self.table_up),
            1   : Button(self.screen, 1450, 545, 220, 100, WHITE, "　▽　", 50, self.table_down),
            2   : Button(self.screen, 1450, 380, 220, 50, WHITE, "△△△", 50, self.table_full_up),
            3   : Button(self.screen, 1450, 650, 220, 50, WHITE, "▽▽▽", 50, self.table_full_down),
        }
        self.bad_view = 0
    #   イベント処理を記述
    def update(self):
        move = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in self.bad_buttons:
                    self.bad_buttons[i].is_clicked(event)
                for i in self.buttons:
                    move = self.buttons[i].is_clicked(event)
                    if move:
                        break
                return move
    
    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        #self.screen.fill((255,255,255))
        self.screen.blit(self.title_text,(50,0))
        self.draw_table()
        for i in self.buttons:
            self.buttons[i].draw()
        if self.view == "error":
            for i in self.bad_buttons:
                self.bad_buttons[i].draw()
        pygame.display.flip()

    def draw_table(self):
        table, get_data = CountList.create_table(self.view)
        self.seting_table(table, get_data)

    def seting_table(self, base_table, base_data):
        data_list = list()
        table = base_table
        for data in base_data:
            for set_data in data:
                data_list.append(set_data)
        if self.view == "error":
            self.bad_cnt = len(data_list)
        for i in range(0,len(table), 1):
            pygame.draw.rect(self.screen, WHITE, table[i])
            pygame.draw.rect(self.screen, BRACK, table[i],1)
            if self.view == "error" and i <= 1:
                self.seting_text(table[i], ERROR[i])
            elif self.view == "error":
                self.seting_text(table[i], str(data_list[(i + self.bad_view) - 2]))
            elif self.view == "today" and i <= 3:
                self.seting_text(table[i], TODAY[i])
            elif self.view == "seven" and i <= 3:
                self.seting_text(table[i], SEVEN[i])
            else:
                self.seting_text(table[i], str(data_list[i - 4]))
    
    def seting_text(self, table, text):
        text_img = self.table_font.render(text, True, BRACK)
        text_rect = text_img.get_rect(center=table.center)
        self.screen.blit(text_img,text_rect)

    #   良否カウント画面に遷移
    def move_today(self):
        self.view = "today"
        self.table_font = pygame.font.Font("C:\\Windows\\Fonts\\msgothic.ttc",size=110)

    def move_seven(self):
        self.bad_view = 0
        self.view = "seven"
        self.table_font = pygame.font.Font("C:\\Windows\\Fonts\\msgothic.ttc",size=50)
    
    def move_error(self):
        self.bad_view = 0
        self.view = "error"
        self.table_font = pygame.font.Font("C:\\Windows\\Fonts\\msgothic.ttc",size=50)

    def table_up(self):
        if self.bad_view > 0:
            self.bad_view -= 2*5
        if self.bad_view < 0:
            self.bad_view = 0
    
    def table_full_up(self):
        if self.bad_view > 0:
            self.bad_view = 0

    def table_down(self):
        if self.bad_view < self.bad_cnt - 14:
            self.bad_view += 2*5
        if self.bad_view > self.bad_cnt - 14:
            self.bad_view = self.bad_cnt - 14
        
    def table_full_down(self):
        if self.bad_view < self.bad_cnt - 14:
            self.bad_view = self.bad_cnt - 14

    #   メインメニューに遷移
    def move_main(self):
        self.bad_view = 0
        self.view = "today"
        return "data"