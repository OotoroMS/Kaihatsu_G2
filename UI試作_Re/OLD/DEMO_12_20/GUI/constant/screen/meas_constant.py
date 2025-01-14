from constant.file_path   import *
from constant.color       import *
# タイトルの設定
MEAS_TITLE_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_meas.png"
}
# ボタンの設定
BACK_BOTTON_STATUS              = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
INDICATOR_BUTTON_STATUS         = {
    "coordinate" : (20,  490),
    "size"       : (360, 250),
    "image_path" : BUTTON_FILE_PATH + "button_indicator.png"
}
MEAS_FORWARD_BUTTON_STATUS      = {
    "coordinate" : (500, 190),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_meas_cylinder_foward.png"
}
SORTING_FORWARD_BUTTON_STATUS   = {
    "coordinate" : (500,  790),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_sorting.png"
}
MEAS_DOWN_BUTTON_STATUS         = {
    "coordinate" : (500, 490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_meas_down.png"
}
MEAS_UP_BUTTON_STATUS           = {
    "coordinate" : (1150,490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_meas_up.png"
}
BUTTON_MEAS_BACK_STATUS         = {
    "coordinate" : (1150,200),
    "size"       : (550, 240),
    "image_path" : BUTTON_FILE_PATH + "button_meas_cylinder_back.png"
}
BUTTON_SORTING_BACK_STATUS      = {
    "coordinate" : (1150,800),
    "size"       : (550, 240),
    "image_path" : BUTTON_FILE_PATH + "button_sorting_back.png"
}
# ランプの設定
TERMINATION  = "動作完了"
MEAS_BACK    = "meas_back"
SORTING_BACK = "sorting_back"

QUERY = "更新クエリを代入"

MEAS_AND_SORT = "測定・分別部"

MEAS_COMAND = {
    "meas_forward"   : ["測定シリンダ前進", MEAS_AND_SORT],
    "sort_forward"   : ["分別シリンダ前進", MEAS_AND_SORT],
    "meas_up"        : ["シリンダ上昇",     MEAS_AND_SORT],
    "meas_down"      : ["シリンダ下降",     MEAS_AND_SORT]
}