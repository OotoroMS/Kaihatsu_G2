from GUI.constants.file_path   import *
from GUI.constants.color       import *

# タイトルの設定
TETLE_MOTION_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_move.png"
}
# 各ボタンの設定
BOTTON_BACK_STATUS         = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
BOTTON_MOTOR_NOMAL_STATUS   = {
    "coordinate" : (160, 350),
    "size"       : (400, 200),
    "image_path" : BUTTON_FILE_PATH + "button_motor_nomal.png"
}
BUTTON_MOTOR_REVERSE_STATUS = {
    "coordinate" : (750, 350),
    "size"       : (400, 200),
    "image_path" : BUTTON_FILE_PATH + "button_motor_reverse.png"
}
BUTTON_ADSORPTION_STATUS    = {
    "coordinate" : (750, 850),
    "size"       : (550, 200),
    "image_path" : BUTTON_FILE_PATH + "button_adsorption_on_off.png"
}
BUTTON_CYLINDER_UP_STATUS   = {
    "coordinate" : (160, 600),
    "size"       : (550, 200),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_up.png"
}
BUTTON_CYLINDER_DOWN_STATUS   = {
    "coordinate" : (750, 600),
    "size"       : (550, 200),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_down.png"
}
# 各画像の設定
EXPTXT_LAMP_STATUS = {
    "coordinate" : (90,   180),
    "size"       : (1150, 400),
    "image_path" : EXP_FILE_PATH + "exptxt_lamp.png"
}
EXPTXT_WORK_IN_STATUS = {
    "coordinate" : (1350, 360),
    "size"       : (400,  170),
    "image_path" : EXP_FILE_PATH + "exptxt_work_in.png"
}
EXPTXT_WORK_OUT_STATUS = {
    "coordinate" : (1350, 610),
    "size"       : (400,  170),
    "image_path" : EXP_FILE_PATH + "exptxt_work_out.png"
}
# ランプの設定
LAMP_MOTOR_LEFT_LIMIT  = {
    "x"     : 240,
    "y"     : 220,
    "w"     : 70,
    "h"     : 70,
    "color" : GRAY
}
LAMP_MOTOR_01 = {
    "x"     : 390,
    "y"     : 220,
    "w"     : 70,
    "h"     : 70,
    "color" : GRAY
}
LAMP_MOTOR_02 = {
    "x"     : 540,
    "y"     : 220,
    "w"     : 70,
    "h"     : 70,
    "color" : GRAY
}
LAMP_MOTOR_03 = {
    "x"     : 690,
    "y"     : 220,
    "w"     : 70,
    "h"     : 70,
    "color" : GRAY
}
LAMP_MOTOR_04 = {
    "x"     : 840,
    "y"     : 220,
    "w"     : 70,
    "h"     : 70,
    "color" : GRAY
}
LAMP_MOTOR_RIGHT_LIMIT = {
    "x"     : 990,
    "y"     : 220,
    "w"     : 70,
    "h"     : 70,
    "color" : GRAY
}
LAMP_CYLINDER_UP = {
    "x"     : 1680,
    "y"     : 420,
    "w"     : 50,
    "h"     : 50,
    "color" : GRAY
}
LAMP_CYLINDER_DOWN = {
    "x"     : 1680,
    "y"     : 670,
    "w"     : 50,
    "h"     : 50,
    "color" : GRAY
}

# ループ終了判定用
TERMINATION  = "動作完了"

BUTTON_ON  = 0
BUTTON_OFF = 1