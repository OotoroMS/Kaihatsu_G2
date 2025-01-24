# import Prometheus
import pygame
import threading

from MAIN_OPRATION.GUI.Constants.screen_name    import *

import MAIN_OPRATION.GUI.MainUIManager as MainUIManager
from SERIAL.serial_gate import SerialGate
OPERATION = "operation"

def MainOpration(prams : dict):
    # ストップイベント
    serial_stop = threading.Event()
    # シリアル通信
    serial_gate = SerialGate(prams, serial_stop)
    # GUI
    gui   = MainUIManager.MainUIManager(serial_gate)
    # バックエンド実行
    stop_event = threading.Event()
    # backend = Prometheus(stop_event)
    # thread = threading.Thread(target=backend.run)
    # シリアル通信開始
    # serial_thread = threading.Thread(target=serial_gate.receive_loop)
    result = gui.run()
    # スレッド実行開始
    # thread.start()
    # serial_thread.start()
    # 終了まで待機
    stop_event.set()
    # thread.join()
    
    # 判別
    if result == MOTION:
        return OPERATION
    return "end"