import pygame
from pygame.locals import *
from SQLCommunication_main import SQLCommunication as DC

SQL = {
    "today" : "select * from db_now",
    "seven" : "select * from db_countlog order by id DESC limit 7",
    "error" : "select * from db_timelog order by id DESC limit 50"
}
TODAY = {
    "px" : 420,#配置
    "py" : 200,
    "x"  : 4,#個数
    "y"  : 2,
    "w"  : 350,#サイズ
    "h"  : 250
}
SEVEN = {
    "px" : 420,
    "py" : 200,
    "x" : 4,
    "y" : 8,
    "w" : 350,
    "h" : 100
}
ERROR = {
    "px" : 420,
    "py" : 200,
    "x" : 2,
    "y" : 8,
    "w" : 525,
    "h" : 100
}
TABLESIZE = {
    "today" : TODAY,
    "seven" : SEVEN,
    "error" : ERROR
}

DBNAME = "testdb_main.db"
DB = DC()

def create_table(target):
    table = _create_frame(target)
    if not table:
        table = False
    data = _get_data(target)
    if not data:
        data = False
    return table, data

#   表の枠を生成
def _create_frame(target):
    lists = list()
    if  target in TABLESIZE:                                            #   辞書に登録されていれば
        size = TABLESIZE[target]                                        #   表のサイズを取得  
        for y in range(0,size["y"],1):                                  #   列数分繰り返し
            top = size["py"] + (size["h"] * y)                          #   高さを取得
            for x in range(0,size["x"],1):                              #   行数分繰り返し
                left = size["px"] + (size["w"] * x)                     #   右の座標を算出
                rect = pygame.Rect(left, top, size["w"], size["h"])     #   枠を生成
                lists.append(rect)                                      #   リストに追加
        return lists
    else:
        return False

def _get_data(target):
    data = list()
    if target in SQL:
        result = DB.table_data_get(DBNAME, SQL[target])
        if target != "error":
            for i in result:
                get_data = [i[1][5:], i[2] + i[3], i[2], i[3]]
                data.append(get_data)
        else:
            cnt = len(result)
            for i in result:
                get_data = [cnt, i[1][5:]]
                data.append(get_data)
                cnt -= 1
        return data
    else:
        return False

def convert_days(days):
    day = ""
    for s in days:
        if s != "-":
            day += s
        else:
            day += "/"