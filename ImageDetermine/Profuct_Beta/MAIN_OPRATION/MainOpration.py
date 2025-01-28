# import Prometheus
import pygame
import threading

from MAIN_OPRATION.GUI.Constants.screen_name    import *

import IMG_DTRMN.ImgDtrmn_Lib as ImgDtrmn_Lib
import MAIN_OPRATION.GUI.MainUIManager as MainUIManager
from SERIAL.serial_gate import SerialGate
OPERATION = "operation"

def MainOpration(prams : dict):
    # ストップイベント(シリアル通信)
    serial_stop = threading.Event()
    # シリアル通信
    serial_gate = SerialGate(prams, serial_stop)
    # GUI
    gui   = MainUIManager.MainUIManager(serial_gate)
    # バックエンド実行
    stop_event = threading.Event()
    print("Stop Event Set")
    backend = ImgDtrmn_Lib.Prometheus(serial_gate,stop_event)
    print("Backend Set")
    thread = threading.Thread(target=backend.run)
    print("Backend Thread Set")
    
    # シリアル通信開始
    serial_thread = threading.Thread(target=serial_gate.receive_loop)
    print("Serial Thread Set")
    
    # スレッド実行開始
    thread.start()
    print("Backend Thread Start")
    serial_thread.start()
    print("Serial Thread Start")

    # GUI開始
    result = gui.run()
    print("GUI Run")
    # 終了まで待機
    stop_event.set()
    serial_stop.set()
    thread.join()
    serial_thread.join()
    
    # 判別
    if result == MOTION:
        return OPERATION
    return "end"