#移動部の動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture

MAINTITLE="GUI_main_test\\image\\title\\pic66.png"
#   メイン画面描画・処理クラス
class Test04Frame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 250, 510, 600, 280, "GUI_main_test\\image\\button\\pic59.png", self.try15),
            Button(self.screen, 1000, 510, 600, 280, "GUI_main_test\\image\\button\\pic60.png", self.try16),
            Button(self.screen, 0, 960, 300, 120, "GUI_main_test\\image\\button\\back.png", self.move_motiontest)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 1000, 220, 600, 230, "GUI_main_test\\image\\button\\pic58.png")
        }
    
    #   動作確認ボタン押下処理
    def try15(self):
        return "try15"
    
    def try16(self):
        return "try16" 

    def move_motiontest(self):
        return "motiontest"