#データ閲覧画面
from DB.SQLCommunication import SQLCommunication
from screen.BaseScreen   import BaseFrame
from parts.Button        import Button
from parts.Picture       import Picture
from constant.FilePath   import *
from constant.ScreenName import *
from constant.PopupName  import *

DATABESE = "testdb_option.db"
QUERY    = "select * from db_now"
BLACK    = ((0,0,0))
GRAY     = ((200,200,200))

#   データ閲覧
class DataFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.db = SQLCommunication()
        self.buttons = {
            Button(self.screen, 150, 300, 700, 350, BUTTONFILEPATH + "pic05.png", self.move_count),#良否カウントログ
            Button(self.screen, 1000, 300, 700, 350, BUTTONFILEPATH + "pic06.png", self.move_graph),#外観検査表示
            Button(self.screen, 0, 960, 330, 120, BUTTONFILEPATH + "back.png", self.move_main)
        }
        self.images = {
            Picture(self.screen, 0, 0, 750, 200,      TITLEFILEPATH  + "pic61.png"),#データ閲覧
            Picture(self.screen, 175, 600, 650, 350,  EXPTXTFILEPATH + "pic69.png"),#カウントログの説明
            Picture(self.screen, 1025, 600, 650, 350, EXPTXTFILEPATH + "pic70.png")#外観検査表示の説明
        }
    
    #   カウントログボタン押下処理
    def move_count(self):
        result = self.db.db_query_execution(DATABESE, QUERY)
        if result:
            return COUNT
        else:
            return NO_DATA
    
    #   寸法検査ログボタン押下処理
    def move_graph(self):
        return IMAGE
    
    def move_main(self):
        return MAIN