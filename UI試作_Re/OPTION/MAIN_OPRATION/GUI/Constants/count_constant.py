# 定数
from MAIN_OPRATION.GUI.Constants.file_path  import *
# 部品
from MAIN_OPRATION.GUI.Parts.Button         import SIZE_SCALE, CORDINATE_SCALE

# CORDINATEのindex
X      = 0
Y      = 1
# SIZEのindex
WIDTH  = 0
HEIGHT = 1
# スクロール機能のON/OFF
ON  = True
OFF = False
# 表示内容
TODAY = "today"
SEVEN = "seven"
ERROR = "error"
# 表のフォントサイズ
FONT_SIZE = {
    TODAY : 110,
    SEVEN : 50,
    ERROR : 50
}
# 各選択ボタンの座標
CORDINATE_TODAY = (20, 280)
CORDINATE_SEVEN = (20, 470)
CORDINATE_ERROR = (20, 660)
# 各選択ボタンのwhidth, height
SIZE_SELECT_BUTTON = (360, 140)
SIZE_SELECT_IMAGE  = (SIZE_SELECT_BUTTON[WIDTH] * SIZE_SCALE, SIZE_SELECT_BUTTON[HEIGHT] * SIZE_SCALE)
# 戻るボタンの設定
BUTTON_BACK_STATUS  = {
    "coordinate" : (0,   960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
# 閲覧記録切替ボタンの設定
BUTTON_TODAY_STATUS = {
    "coordinate" : CORDINATE_TODAY,
    "size"       : SIZE_SELECT_BUTTON,
    "image_path" : BUTTON_FILE_PATH + "button_today.png"
}
BUTTON_SEVEN_STATUS = {
    "coordinate" : CORDINATE_SEVEN,
    "size"       : SIZE_SELECT_BUTTON,
    "image_path" : BUTTON_FILE_PATH + "button_seven.png"
}
BUTTON_ERROR_STATUS = {
    "coordinate" : CORDINATE_ERROR,
    "size"       : SIZE_SELECT_BUTTON,
    "image_path" : BUTTON_FILE_PATH + "button_error.png"
}
# スクロールボタンの設定
BUTTON_FULLUP_SCROL_STATUS   = {
    "coordinate" : (1570,280),
    "size"       : (220, 160),
    "image_path" : BUTTON_FILE_PATH + "button_fullup.png"
}
BUTTON_UP_SCROL_STATUS       = {
    "coordinate" : (1590,480),
    "size"       : (180, 130),
    "image_path" : BUTTON_FILE_PATH + "button_up.png"
}
BUTTON_DOWN_SCROL_STATUS     = {
    "coordinate" : (1590,640),
    "size"       : (180, 130),
    "image_path" : BUTTON_FILE_PATH + "button_down.png"
}
BUTTON_FULLDOWN_SCROL_STATUS = {
    "coordinate" : (1570,810),
    "size"       : (220, 160),
    "image_path" : BUTTON_FILE_PATH + "button_fulldown.png"
}
# 現在の表示内容の設定
IMAGE_TODAY_STATUS  = {
    "coordinate" : (CORDINATE_TODAY[X]  - (SIZE_SELECT_BUTTON[WIDTH] * CORDINATE_SCALE) // 2, CORDINATE_TODAY[Y] - (SIZE_SELECT_BUTTON[HEIGHT] * CORDINATE_SCALE) // 2),
    "size"       : SIZE_SELECT_IMAGE,
    "image_path" : EXPTXT_FILE_PATH + "exptxt_today.png"
}
IMAGE_SEVEN_STATUS  = {
    "coordinate" : (CORDINATE_SEVEN[X]  - (SIZE_SELECT_BUTTON[WIDTH] * CORDINATE_SCALE) // 2, CORDINATE_SEVEN[Y] - (SIZE_SELECT_BUTTON[HEIGHT] * CORDINATE_SCALE) // 2),
    "size"       : SIZE_SELECT_IMAGE,
    "image_path" : EXPTXT_FILE_PATH + "exptxt_seven.png"
}
IMAGE_ERROR_STATUS  = {
    "coordinate" : (CORDINATE_ERROR[X]  - (SIZE_SELECT_BUTTON[WIDTH] * CORDINATE_SCALE) // 2, CORDINATE_ERROR[Y] - (SIZE_SELECT_BUTTON[HEIGHT] * CORDINATE_SCALE) // 2),
    "size"       : SIZE_SELECT_IMAGE,
    "image_path" : EXPTXT_FILE_PATH + "exptxt_error.png"
}
# タイトル
COUNT_TITLE_STAUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_count.png"
}
# データ確認用QUERY
QUERY = {
    SEVEN : "select * from db_countlog order by id DESC limit 7",
    ERROR : "select * from db_timelog order by id DESC limit 50"
}