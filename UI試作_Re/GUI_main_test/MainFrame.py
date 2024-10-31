#メインメニュー
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
MAINTITLE=".\\image\\title\\pic03.png"
#   メイン画面描画・処理クラス
class MainFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 150, 300, 700, 350, ".\\image\\button\\pic01.png", self.move_data),
            Button(self.screen, 1000, 300, 700, 350, ".\\image\\button\\pic02.png", self.move_pass),
            Button(self.screen, 0, 960, 330, 120, ".\\image\\button\\pic04.png", self.end_app)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 175, 600, 650, 350, ".\\image\\exptxt\\pic67.png"),
            Picture(self.screen, 1025, 600, 650, 350, ".\\image\\exptxt\\pic68.png")
        }
    
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
        return "end"