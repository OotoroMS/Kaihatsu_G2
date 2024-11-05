#動作確認画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture

BLACK = ((0,0,0))
GRAY  = ((200,200,200))
MAINTITLE="GUI_main_test\\image\\title\\pic62.png"
#   メイン画面描画・処理クラス
class MotionTestFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 50, 650, 330, 150, "GUI_main_test\\image\\button\\pic33.png", self.move_test01),
            Button(self.screen, 570, 170, 330, 150, "GUI_main_test\\image\\button\\pic34.png", self.move_test02),
            Button(self.screen, 670, 850, 330, 150, "GUI_main_test\\image\\button\\pic35.png", self.move_test03),
            Button(self.screen, 1100, 270, 330, 150, "GUI_main_test\\image\\button\\pic36.png", self.move_test04),
            Button(self.screen, 1570, 710, 330, 150, "GUI_main_test\\image\\button\\pic74.png", self.dbreset),
            Button(self.screen, 1570, 900, 330, 150, "GUI_main_test\\image\\button\\pic37.png", self.move_changepass),
            Button(self.screen, 0, 960, 330, 120, "GUI_main_test\\image\\button\\back.png", self.move_main)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, MAINTITLE),
            Picture(self.screen, 250, 210, 1300, 740, "GUI_main_test\\image\\exptxt\\pic32.png")
        }
    
    #   動作確認ボタン押下処理
    def move_test01(self):
        return "test01"
    
    def move_test02(self):
        return "test02"

    def move_test03(self):
        return "test03"
    
    def move_test04(self):
        return "test04"

    def dbreset(self):
        return "dbreset"    

    def move_changepass(self):
        return "changepass"

    def move_main(self):
        return "main"