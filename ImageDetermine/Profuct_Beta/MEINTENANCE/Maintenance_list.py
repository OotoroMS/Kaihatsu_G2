import pygame
import threading
import queue
import time
from SERIAL.manager.SerialUIBridge      import SerialUIBridge
from MEINTENANCE.GUI.ListUIManager          import UIMabager
from MEINTENANCE.BACK.BackEndManager_list    import BackEndManager

class SerialRead:
    def __init__(self, serial : SerialUIBridge):
        self.serial         = serial
        self.loop_flg       = True
        self.in_flg = False
        
    # 受信
    def read(self):
            print("Maintenance.py class:SerialRead def:read text: SerialRead Start")
            while self.loop_flg:
                self.serial.read_loop()
                time.sleep(0.1)
            self.serial.serial_close()
            print("Maintenance.py class:SerialRead def:read text: SerialRead End")

    # 終了処理
    def end_loop(self):
        self.loop_flg = False

def Maintenance(prms : dict):
        # キュー
        ui_backend_que      = queue.Queue() # PC-PLCの生成
        backend_ui_que      = queue.Queue() # PLC-PCの生成
        work_ui_backend_que = queue.Queue() # ワーク関係送信キューの生成
        work_backend_ui_que = queue.Queue() # ワーク関係受信キューの生成
        opretion_ui_backend_que = queue.Queue() # メンテナンス関係送信キューの生成
        opretion_backend_ui_que = queue.Queue() # メンテナンス関係受信キューの生成
        ui_backend_lock = threading.Lock()
        backend_ui_lock = threading.Lock()
        work_ui_backend_lock = threading.Lock()
        work_backend_ui_lock = threading.Lock()
        opretion_ui_backend_lock = threading.Lock()
        opretion_backend_ui_lock = threading.Lock()

        UIBridge = SerialUIBridge(prms)
        # シリアル通信受信スレッド
        serial_read     = SerialRead(UIBridge)
        # GUI表示クラス
        gui             = UIMabager([ui_backend_que, backend_ui_que], [ui_backend_lock, backend_ui_lock], [work_ui_backend_que, work_backend_ui_que], [work_ui_backend_lock, work_backend_ui_lock], [opretion_ui_backend_que, opretion_backend_ui_que], [opretion_ui_backend_lock, opretion_backend_ui_lock])
        # バックエンド処理クラス
        backendManager  = BackEndManager([backend_ui_que, ui_backend_que], [backend_ui_lock, ui_backend_lock], [work_backend_ui_que, work_ui_backend_que], [work_backend_ui_lock, work_ui_backend_lock], [opretion_backend_ui_que, opretion_ui_backend_que], [opretion_backend_ui_lock, opretion_ui_backend_lock], serial=UIBridge)
        # バックグラウンドスレッド生成
        back_thread     = threading.Thread(target=backendManager.run)
        # シリアル通信受信スレッド生成
        serial_thread   = threading.Thread(target=serial_read.read)
        # スレッド開始
        serial_thread.start()
        back_thread.start()
        
        # UI表示
        gui.run()

        
        # スレッドが終了するまで待機
        back_thread.join()

        # 終了処理
        serial_read.end_loop()
        serial_thread.join()
        
        print("Maintenance.py class:Maintenance def:Maintenance text: Maintenance End")

if __name__ == "__main__":
        pygame.init()
        Maintenance()
        pygame.quit()