# import Prometheus
import pygame
import threading

from MAIN_OPRATION.GUI.Constants.screen_name    import *

import Prometheus.Prometheus as Prometheus
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
    backend = Prometheus.Prometheus(stop_event)
    thread = threading.Thread(target=backend.run)
    # シリアル通信開始
    serial_thread = threading.Thread(target=serial_gate.receive_loop)
    
    # スレッド実行開始
    thread.start()
    serial_thread.start()
    result = gui.run()
    # 終了まで待機
    stop_event.set()
    serial_stop.set()
    thread.join()
    serial_thread.join()
    
    # 判別
    if result == MOTION:
        return OPERATION
    return "end"