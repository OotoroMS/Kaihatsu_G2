#メインメニュー
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture
from BasePopup import BasePopup
import pygame
BLACK = ((0,0,0))
GRAY  = ((200,200,200))
MAINTITLE="GUI_main_test\\image\\title\\pic03.png"
POPUPMSSEGE = "パスワードが違います" 
#   メイン画面描画・処理クラス
class MainFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.flg_veiw_popup = False
        self.popup_different_pass = BasePopup(self.screen, font, POPUPMSSEGE)
        self.buttons = {
            Button(self.screen, 150, 300, 700, 350, "GUI_main_test\\image\\button\\pic01.png", self.move_data),
            Button(self.screen, 1000, 300, 700, 350, "GUI_main_test\\image\\button\\pic02.png", self.move_pass),
            Button(self.screen, 0, 960, 330, 120, "GUI_main_test\\image\\button\\pic04.png", self.end_app)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 175, 600, 650, 350, "GUI_main_test\\image\\exptxt\\pic67.png"),
            Picture(self.screen, 1025, 600, 650, 350, "GUI_main_test\\image\\exptxt\\pic68.png")
        }
    
    #   ボタン及びテキストの描画処理を記述
    def draw(self):
        for image in self.images:
            image.draw()
        for button in self.buttons:
            button.draw()
        if self.flg_veiw_popup:
            self.popup_different_pass.draw()
            self.flg_veiw_popup = self.popup_different_pass.update()


    #   データ一覧ボタン押下処理
    def move_data(self):
        print("return data")
        return "data"
    
        #   動作確認ボタン押下処理
    def move_pass(self):
        print("return pass")
        return "pass"
    
    def end_app(self):
        print("return end")
        while 1:
            self.popup_different_pass.draw()
            result = self.popup_different_pass.update()
            if "YES"  == result:#はいが押された時FALSE
                return "end"
            elif "NO" == result:
                return "main"
            pygame.display.update()
        # return "end"