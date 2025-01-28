from MAIN_OPRATION.GUI.Constants.file_path   import *

PASSINPUTMAX   = 11
PASS_FONT_SIZE = 80
NUM_BUTTONS_X = [660, 850, 1040]
NUM_BUTTONS_Y = [750, 570, 390]
NUM_BUTTONS_SIZE = (180,180)
NUM_BUTTONS_FILE_PATH = [
    BUTTON_FILE_PATH + "button_1.png",
    BUTTON_FILE_PATH + "button_2.png",
    BUTTON_FILE_PATH + "button_3.png",
    BUTTON_FILE_PATH + "button_4.png",
    BUTTON_FILE_PATH + "button_5.png",
    BUTTON_FILE_PATH + "button_6.png",
    BUTTON_FILE_PATH + "button_7.png",
    BUTTON_FILE_PATH + "button_8.png",
    BUTTON_FILE_PATH + "button_9.png",
]

PASS_TITLE_STATUS  = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_pass.png"
}
BACK_BOTTON_STATUS = {
    "coordinate" : (0, 960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}
ZERO_BUTON_STATUS  = {
    "coordinate" : (660, 915),
    "size"       : (370, 200),
    "image_path" : BUTTON_FILE_PATH + "button_0.png"
}
CLR_BUTTON_STATUS  = {
    "coordinate" : (1230,390),
    "size"       : (175, 173),
    "image_path" : BUTTON_FILE_PATH + "button_clr.png"
}
ENT_BUTTON_STATUS  = {
    "coordinate" : (1211,570),
    "size"       : (212, 360),
    "image_path" : BUTTON_FILE_PATH + "button_ent.png"
}
ROCK_EXPEXT_STATUS = {
    "coordinate" : (410, 200),
    "size"       : (180, 180),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_rock.png"
}

QUERY        = "select num from pass_num"