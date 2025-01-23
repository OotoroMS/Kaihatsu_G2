import pygame
import threading
import queue
import serial
from SERIAL.manager.SerialUIBridge      import SerialUIBridge
from MEINTENANCE.GUI.UIManager          import UIMabager
from MEINTENANCE.BACK.BackEndManager    import BackEndManager

class SerialRead:
    def __init__(self, serial : SerialUIBridge):
        self.serial         = serial
        self.loop_flg       = True
    # 受信
    def read(self):
            while self.loop_flg:
                self.serial.read_loop()
    # 終了処理
    def end_loop(self):
        self.loop_flg = False

def Maintenance(prms : dict):
        # キュー
        ui_backend_que  = queue.Queue()
        backend_ui_que  = queue.Queue()
        ui_backend_lock = threading.Lock()
        backend_ui_lock = threading.Lock()

        UIBridge = SerialUIBridge(prms)

        gui             = UIMabager(send_que=ui_backend_que, recv_que=backend_ui_que, send_lock=ui_backend_lock, recv_lock=backend_ui_lock)
        backendManager  = BackEndManager(send_que=backend_ui_que, recv_que=ui_backend_que, send_lock=backend_ui_lock, recv_rock=ui_backend_lock, serial=UIBridge)

        back_thread     = threading.Thread(target=backendManager.run)
        # スレッド開始
        back_thread.start()
        
        # UI表示
        gui.run()

        # スレッドが終了するまで待機
        back_thread.join()

if __name__ == "__main__":
        pygame.init()
        Maintenance()
        pygame.quit()