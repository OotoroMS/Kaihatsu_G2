import pygame
from BaseFrame import BaseFrame
from Button import Button
from NumButton import NumButton
from BasePopup import BasePopup
BLACK = ((0,0,0))
GRAY  = ((200,200,200))
POPUPMSSEGE = "パスワードが違います" 
#   メイン画面描画・処理クラス
class PassFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.text_title = self.font_title.render("パスワード入力", True, BLACK)
        self.pass_font = pygame.font.Font(font, 60)
        self.pass_rect = pygame.rect.Rect(710, 200, 500, 150)
        self.set_pass = ""
        self.flg_veiw_popup = False
        self.popup_different_pass = BasePopup(self.screen, font, POPUPMSSEGE)  
        self.buttons = {
            Button(self.screen, 1570, 930, 330, 120, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\return.png", self.move_main),
            NumButton(self.screen, 910,  690, 100, 100, GRAY, "0", 90, self.num_0),
            NumButton(self.screen, 810,  390, 100, 100, GRAY, "1", 90, self.num_1),
            NumButton(self.screen, 910,  390, 100, 100, GRAY, "2", 90, self.num_2),
            NumButton(self.screen, 1010, 390, 100, 100, GRAY, "3", 90, self.num_3),
            NumButton(self.screen, 810,  490, 100, 100, GRAY, "4", 90, self.num_4),
            NumButton(self.screen, 910,  490, 100, 100, GRAY, "5", 90, self.num_5),
            NumButton(self.screen, 1010, 490, 100, 100, GRAY, "6", 90, self.num_6),
            NumButton(self.screen, 810,  590, 100, 100, GRAY, "7", 90, self.num_7),
            NumButton(self.screen, 910,  590, 100, 100, GRAY, "8", 90, self.num_8),
            NumButton(self.screen, 1010, 590, 100, 100, GRAY, "9", 90, self.num_9),
            NumButton(self.screen, 1110, 390, 100, 100, GRAY, "CLR", 50, self.num_clr),
            NumButton(self.screen, 1110, 490, 100, 200, GRAY, "ENTER", 30, self.num_check)
        }
    
    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        self.screen.blit(self.text_title,(200,50))
        self.draw_pass()
        for button in self.buttons:
            button.draw()
        if self.flg_veiw_popup:
            self.popup_different_pass.draw()
            self.flg_veiw_popup = self.popup_different_pass.update()

    def draw_pass(self):
        self.passward = self.pass_font.render(self.set_pass, True, BLACK)
        self.pass_center = self.passward.get_rect(center=self.pass_rect.center)
        pygame.draw.rect(self.screen, (255,255,255), self. pass_rect)   #   稼働状況更新の領域を確保
        pygame.draw.rect(self.screen, BLACK, self.pass_rect, 1)         #   外枠を描画
        self.screen.blit(self.passward,self.pass_center)

    def move_main(self):
        self.set_pass = ""
        return "main"
    
    def num_0(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "0"
    def num_1(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "1"
    def num_2(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "2"
    def num_3(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "3"
    def num_4(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "4"
    def num_5(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "5"
    def num_6(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "6"
    def num_7(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "7"
    def num_8(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "8"
    def num_9(self):
        if len(self.set_pass) <= 15:
            self.set_pass += "9"
    
    def num_clr(self):
        self.set_pass = ""
    
    def num_check(self):
        if self.set_pass == "2024":
            self.set_pass = ""
            return "test"
        else:
            self.set_pass = ""
            self.flg_veiw_popup = True