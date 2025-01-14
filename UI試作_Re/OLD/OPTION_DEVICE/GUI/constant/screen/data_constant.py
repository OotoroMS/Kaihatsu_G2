from constant.file_path import *

DATA_TETLE_STATUS    = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_data.png"
}
EXPTXT_DATA_STATUS   = {
    "coordinate" : (175, 600),
    "size"       : (650, 350),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_count.png"
}
EXPTXT_VISION_STATUS  = {
    "coordinate" : (1025,600),
    "size"       : (650, 350),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_vision.png"
}
BUTTON_COUNT_STATUS  = {
    "coordinate" : (150, 300),
    "size"       : (700, 350),
    "image_path" : BUTTON_FILE_PATH + "button_count.png"
}
BUTTON_VISION_STATUS  = {
    "coordinate" : (1000,300),
    "size"       : (700, 350),
    "image_path" : BUTTON_FILE_PATH + "button_vision.png"
}
BUTTON_BACK_STATUS   = {
    "coordinate" : (0,   960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}

# パスワード認証用
QUERY = "select * from db_now"