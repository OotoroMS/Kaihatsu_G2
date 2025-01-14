#データ閲覧画面
from BaseFrame import BaseFrame
from Button import Button
from Picture import Picture

BLACK = ((0,0,0))
GRAY  = ((200,200,200))

#   データ閲覧
class DataFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 150, 300, 700, 350, "GUI_main_test\\image\\button\\pic05.png", self.move_count),#良否カウントログ
            Button(self.screen, 1000, 300, 700, 350, "GUI_main_test\\image\\button\\pic06.png", self.move_graph),#寸法測定ログ
            Button(self.screen, 0, 960, 330, 120, "GUI_main_test\\image\\button\\back.png", self.move_main)#戻る
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200, "GUI_main_test\\image\\title\\pic61.png"),#データ閲覧
            Picture(self.screen, 175, 600, 650, 350, "GUI_main_test\\image\\exptxt\\pic69.png"),#良否判定,不良発生を閲覧
            Picture(self.screen, 1025, 600, 650, 350, "GUI_main_test\\image\\exptxt\\pic70.png")#寸法グラフを表示
        }
    
    #   カウントログボタン押下処理
    def move_count(self):
        print("return count")
        return "count"
    
    #   寸法検査ログボタン押下処理
    def move_graph(self):
        print("return graph")
        return "graph"
    #メインメニューに戻る
    def move_main(self):
        return "main"