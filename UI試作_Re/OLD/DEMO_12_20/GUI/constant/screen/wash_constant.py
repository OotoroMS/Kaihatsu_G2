from constant.file_path   import *
from constant.color       import *
# タイトルの設定
WASH_TITLE_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_wash.png"
}

# ボタンの設定
BACK_BOTTON_STATUS                = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
ECCENTRICITY_BUTTON_STATUS        = {
    "coordinate" : (1100,190),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_eccentricity.png"
}
CYRINDER_ADVANCE_BUTTON_STATUS    = {
    "coordinate" : (350, 490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_advance.png"
}
CYRINDER_RETRACTION_BUTTON_STATUS = {
    "coordinate" : (1100,490),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_cylinder_retraction.png"
}
PUMP_BUTTON_STATUS                = {
    "coordinate" : (350, 790),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_pump.png"
}
AIR_BLOW_BUTTON_STATUS            = {
    "coordinate" : (1100,790),
    "size"       : (550, 250),
    "image_path" : BUTTON_FILE_PATH + "button_air.png"
}
# 画像の設定
CATCH_EXPTXT_STATUS = {
    "coordinate" : (50,  220),
    "size"       : (400, 200),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_catch.png"
}
WORK_EXPTXT_STATUS  = {
    "coordinate" : (500, 220),
    "size"       : (400, 200),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_work.png"
}
# ランプの設定
CATCH_LAMP_STATUS = {
    "x"     : 380,
    "y"     : 295,
    "w"     : 50,
    "h"     : 50,
    "color" : GRAY
    }
WORK_LAMP_STATUS  = {
    "x"      : 825,
    "y"      : 295,
    "w"      : 50,
    "h"      : 50,
    "color"  : GRAY
    }

TERMINATION = "動作完了"

WORK_LAMP   = "work"
CATCH_LAMP  = "catch"
IN_AND_WASH = "投入洗浄部"

# 命令一覧
WASH_SCREEN_COMMAND = {
    "cylinder_advance"      : ("押出シリンダ前進" , "投入・洗浄部"),
    "cylinder_retraction"   : ("押出シリンダ後退" , "投入・洗浄部") ,
    "eccentricity"          : ("偏芯モータ回転"   , "投入・洗浄部"),
    "pump"                  : ("ポンプ"           , "投入・洗浄部"),
    "air_brow"              : ("エアブロー"       , "投入・洗浄部")
}