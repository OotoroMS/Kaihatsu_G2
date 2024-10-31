from BaseFrame import BaseFrame
from Button import Button

BLACK = ((0,0,0))
GRAY  = ((200,200,200))

#   メイン画面描画・処理クラス
class MainFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.text_title = self.font_title.render("検査・蓄積収納装置", True, BLACK)
        self.buttons = {
            Button(self.screen, 150, 200, 700, 200, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\data.png", self.move_data),
            Button(self.screen, 150, 550, 700, 200, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\pass.png", self.move_pass),
            Button(self.screen, 1570, 930, 330, 120, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\end.png", self.end_app)
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