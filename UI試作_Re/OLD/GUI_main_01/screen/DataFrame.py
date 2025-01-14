#データ閲覧
from screen.BaseFrame import BaseFrame
from parts.Button import Button
from parts.Picture import Picture
from parts.SQLCommunication_main import SQLCommunication
from filepath import *

BLACK = ((0,0,0))
GRAY  = ((200,200,200))

COUNTQUERY = "select * from db_now"

GRAPHQUERY = "select * from DB_sizelog order by id desc limit 20"

DBNAME =  "testdb_main.db"

#   データ閲覧
class DataFrame(BaseFrame):
    def __init__(self, screen, font=None):
        super().__init__(screen, font)
        self.buttons = {
            Button(self.screen, 150,  300, 700, 350, IMAGEFILEPATH + "button\\pic05.png", self.move_count),
            Button(self.screen, 1000, 300, 700, 350, IMAGEFILEPATH + "button\\pic06.png", self.move_graph),
            Button(self.screen, 0,    960, 330, 120, IMAGEFILEPATH + "button\\back.png", self.move_main)
        }
        self.images = {
            Picture(self.screen, 0,    0,   750, 200,  IMAGEFILEPATH + "title\\pic61.png"),
            Picture(self.screen, 175,  600, 650, 350,  IMAGEFILEPATH + "exptxt\\pic69.png"),
            Picture(self.screen, 1025, 600, 650, 350,  IMAGEFILEPATH + "exptxt\\pic70.png")
        }
        self.db = SQLCommunication()
    
    #   カウントログボタン押下処理
    def move_count(self):
        result = self.db.db_query_execution(DBNAME, COUNTQUERY)
        if not result:
            return "none_data"
        return "count"
    
    #   寸法検査ログボタン押下処理
    def move_graph(self):
        result = self.db.db_query_execution(DBNAME, GRAPHQUERY)
        if not result:
            return "none_data"
        return "graph"
    
    def move_main(self):
        return "main"