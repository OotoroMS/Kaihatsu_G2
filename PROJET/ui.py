# ui.py

import threading
from queue import Queue
import pygame
import serial

# 自作プログラムをimport
# Application と background_task のインポート
from GUI.FRONT.Application import Application
from GUI.BACK.test import background_task
from SERIAL.manager.serial_communicator import SerialCommunicator

def main():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

    # フロントとバックのキュー
    to_back = Queue()
    from_back = Queue()
    
    serial_params1 = {
        "port": "COM4",
        "baudrate": 9600,
        "parity": serial.PARITY_NONE,
        "stopbits": serial.STOPBITS_ONE,
        "timeout": 0.08,
    }
    serial_comm = SerialCommunicator(**serial_params1)

    # Application のインスタンス化
    app = Application(screen, to_back, from_back)

    # スレッドでバックエンドの処理を開始
    backend_thread = threading.Thread(target=background_task, args=(to_back, from_back, serial_comm))
    backend_thread.daemon = True  # メインスレッドが終了するとバックグラウンドスレッドも終了
    backend_thread.start()

    # アプリケーションのメインループを実行
    app.run()

if __name__ == "__main__":
    main()
