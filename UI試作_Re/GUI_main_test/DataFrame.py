from BaseFrame import BaseFrame
from Button import Button

BLACK = ((0,0,0))
GRAY  = ((200,200,200))

#   メイン画面描画・処理クラス
class DataFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.text_title = self.font_title.render("データ一覧", True, BLACK)
        self.buttons = {
            Button(self.screen, 150, 200, 700, 200, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\count.png", self.move_count),
            Button(self.screen, 150, 550, 700, 200, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\measlog.png", self.move_graph),
            Button(self.screen, 1570, 930, 330, 120, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\return.png", self.move_main)
        }
    
    #   カウントログボタン押下処理
    def move_count(self):
        print("return count")
        return "count"
    
    #   寸法検査ログボタン押下処理
    def move_graph(self):
        print("return graph")
        return "graph"
    
    def move_main(self):
        return "main"