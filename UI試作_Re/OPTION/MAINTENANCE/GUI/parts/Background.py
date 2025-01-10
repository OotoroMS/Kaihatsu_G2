# 背景の切替・描画を行うクラス
import pygame
from typing                     import Tuple,Optional
from GUI.constants.screen_name  import *
from GUI.constants.file_path    import *

BASE     = "base"
PASSWORD = "password"

BACKGROND_SCCREEN     = {
    MAIN    : BASE,
    VISION  : BASE,
    MOVE    : BASE,
    CHANGE  : PASSWORD 
}

BACKGROUND_IMAGE_PATH = {
    BASE     : BACKGROUND_FILE_PATH + "base.jpg",
    PASSWORD : BACKGROUND_FILE_PATH + "password.jpg"
}

ORIGEN = (0,0)

def setting_backgrond(current_screen) -> Optional[pygame.Surface]:
    if current_screen in BACKGROND_SCCREEN.keys():
        key = BACKGROND_SCCREEN[current_screen]
        if key in BACKGROUND_IMAGE_PATH.keys():
            return load_image(key)
    print("BACKGROND_SCREENにキーとして登録されていません")
    return None

def load_image(key : str) -> Optional[pygame.Surface]:
    try:
        window_size = pygame.display.get_window_size()
        image = pygame.image.load(BACKGROUND_IMAGE_PATH[key])
        return pygame.transform.scale(image, window_size)
    except Exception as e:
        print("load_image error: ", e)
        return None