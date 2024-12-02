import pygame
from typing import Tuple, Optional
# 定数
from GUI.constant.file_path         import *
from GUI.constant.color             import *
from GUI.constant.popup.popup_name  import *
# 部品
from GUI.parts.Button           import *
from GUI.parts.Picture          import *
from GUI.parts.CaluclatePopup   import *

WORNING_IMAGE = {
    "size"       : (380, 280),
    "image_path" : EXPTXT_FILE_PATH + "error.png"
}