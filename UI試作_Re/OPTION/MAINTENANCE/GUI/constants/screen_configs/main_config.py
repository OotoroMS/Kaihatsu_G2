# メイン画面の定数
# ファイルパス
from GUI.constants.file_path    import *
from GUI.constants.color        import *
# タイトルの設定
TITLE_MAIN_CONFIG = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_select.png"
}
# 戻るボタン
BUTTON_BACK_CONFIG = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
# パスワード変更画面遷移ボタン
BUTTON_CHANGE_PASS_CONFIG = {
    "coordinate" : (1570,900),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_change.png"
}
BUTTON_RESET_CONFIG = {
    "coordinate" : (1570,710),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_dbreset.png"
}
# 移動部遷移ボタン
BUTTON_MOVING_CONFIG = {
    "coordinate" : (500, 830),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_moving.png"
}
# 外観検査部遷移ボタン
BUTTON_VISION_CONFIG = {
    "coordinate" : (950, 830),
    "size"       : (330, 150),
    "image_path" : BUTTON_FILE_PATH + "button_vision.png"
}

# 各種画像の設定
EXP_TARGET_CONFIG = {
    "coordinate" : (250, 210),
    "size"       : (1300,740),
    "image_path" : EXP_FILE_PATH + "exptxt_target.png"
}
# 線の瀬鄭
LINE_RED_CONFIG = {
    "color"     : RED,
    "start_pos" : (665,  850),
    "end_pos"   : (1050, 500),
    "width"     : 8
}
LINE_BLUE_CONFIG = {
    "color"     : BLUE,
    "start_pos" : (1115, 850),
    "end_pos"   : (1200, 600),
    "width"     : 8
}
