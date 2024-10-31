from BaseFrame import BaseFrame
from Button import Button
from Lamp import Lamp
BLACK = ((0,0,0))
GRAY  = ((200,200,200))

YEROW = ((255,255,0)) 
GREEN = ((0,255,0))

COLOR = ((YEROW))

#   メイン画面描画・処理クラス
class TestFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.text_title = self.font_title.render("機能テスト", True, BLACK)
        self.buttons = {
            Button(self.screen, 150, 200, 700, 200, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\count.png", self.change_color),
            Button(self.screen, 1570, 930, 330, 120, "D:\\Kaihatsu\\VScode\\GUI\\GUI_main_test\\image\\return.png", self.move_main)
        }
        self.lamps = list((
            Lamp(self.screen, 865, 200, YEROW),
            Lamp(self.screen, 865, 300, YEROW)
        ))
        self.color = YEROW
    
#      ボタン及びテキストの描画処理を記述
    def draw(self):
        self.screen.blit(self.text_title,(200,10))
        for button in self.buttons:
            button.draw()
        for lamp in self.lamps:
            lamp.draw()
    
    #   カウントログボタン押下処理
    def change_color(self):
        if self.color == YEROW:
            self.color = GREEN
        else:
            self.color = YEROW
        
        self.lamps[0].update_color(self.color)
    
    def move_main(self):
        return "main"