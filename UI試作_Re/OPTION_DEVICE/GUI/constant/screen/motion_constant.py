from GUI.constant.file_path   import *
from GUI.constant.color       import *
# タイトルの設定
TETLE_MOTION_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_motion.png"
}
# 各ボタンの設定
BOTTON_BACK_STATUS  = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
RESET_BUTTON_STATUS = {
    "coordinate" : (1570,710),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_dbreset.png"
}
PASS_BUTTON_STATUS  = {
    "coordinate" : (1570,900),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_change.png"
}
BUTTON_MOVE_STATUS = {
    "coordinate" : (500, 830),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_motion_move.png"
}
BUTTON_VISION_STATUS = {
    "coordinate" : (950, 830),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_motion_vision.png"
}
# 各種画像の設定
EXPTXT_TARGET_STATUS = {
    "coordinate" : (250, 210),
    "size"       : (1300,740),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_target.png"
}
# データベース関係
QUERY = "DELETE FROM %s"
TARGETTABLE = [
    "db_now",
    "db_countlog",
    "db_timelog",
    "db_sizelog"
]
# 線の設定
LINE_RED_STATUS = {
    "color"     : RED,
    "start_pos" : (665,  850),
    "end_pos"   : (1050, 500),
    "width"     : 8
}
LINE_BLUE_STATUS = {
    "color"     : BLUE,
    "start_pos" : (1115, 850),
    "end_pos"   : (1200, 600),
    "width"     : 8
}