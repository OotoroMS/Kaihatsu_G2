import pygame
import threading
import queue

from GUI.UIManager              import UIMabager
from BACK.BackEndManager        import BackEndManager
def Maintenance():
        
        # キュー
        ui_backend_que  = queue.Queue()
        backend_ui_que  = queue.Queue()
        ui_backend_lock = threading.Lock()
        backend_ui_lock = threading.Lock()

        gui             = UIMabager(send_que=ui_backend_que, recv_que=backend_ui_que, send_lock=ui_backend_lock, recv_lock=backend_ui_lock)
        backendManager  = BackEndManager(send_que=backend_ui_que, recv_que=ui_backend_que, send_lock=backend_ui_lock, recv_rock=ui_backend_lock)

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