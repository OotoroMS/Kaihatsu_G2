# import Prometheus
import pygame
import threading

from MAIN_OPRATION.GUI.Constants.screen_name    import *

import MAIN_OPRATION.GUI.MainUIManager as MainUIManager
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
OPERATION = "operation"

def MainOpration():
    pass
    gui   = MainUIManager.MainUIManager()
    # バックエンド実行
    # backend = Prometheus()
    # thread = threading.Thread(target=backend.run)
    result = gui.run()
    # thread.start()
    # 終了まで待機
    # thread.join()
    
    # 判別
    if result == MOTION:
        return OPERATION
    return "end"