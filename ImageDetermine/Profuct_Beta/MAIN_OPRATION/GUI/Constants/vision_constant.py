from MAIN_OPRATION.GUI.Constants.file_path import *
from MAIN_OPRATION.GUI.Constants.color     import *

TITLE_VISION_STATUS = {
    "coordinate" : (0,   0),
    "size"       : (750, 200),
    "image_path" : TITLE_FILE_PATH + "title_vision.png"
}
EXPTXT_NO_IMAGE_STATUS = {
    "coordinate" : ((1920-1296)//2,  ((1080-972+972*0.15)//2) + 20),
    "size"       : (1296, int(972*0.85)),
    "image_path" : EXPTXT_FILE_PATH + "no_image.png"
}
BUTTON_BACK_STATUS = {
    "coordinate" : (0,   960),
    "size"       : (330, 120),
    "image_path" : BUTTON_FILE_PATH + "button_back.png"
}

ZERO = 0