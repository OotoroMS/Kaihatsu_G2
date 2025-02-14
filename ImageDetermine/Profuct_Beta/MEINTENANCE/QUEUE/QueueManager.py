# キューの管理を行うクラス
# キューによるデータの送信及び受信を行う
import queue
import threading
# 定数
from MEINTENANCE.CONSTANTS.pless_command    import *
from MEINTENANCE.CONSTANTS.command_type     import *
from MEINTENANCE.CONSTANTS.serial_result    import *

class QueueManager:
    def __init__(self, send_que : queue.Queue, recv_que : queue.Queue, send_lock : threading.Lock, recv_lock : threading.Lock) -> None:
        # 送受信キュー
        self.send_que = send_que
        self.recv_que = recv_que
        # スレッドロック
        self.send_lock = send_lock
        self.recv_lock = recv_lock

    # 送信(汎用)
    def send_message(self, message):
        with self.send_lock:
            self.send_que.put(message)
    
    # 受信(汎用)
    def recv_message(self):
        if not self.recv_que.empty():
            with self.recv_lock:
                # print("QueueManager.py recv_message : get messsage")
                return self.recv_que.get()
        return ""
    
    # 何か受信するまで繰り返す
    def until_recv_message(self):
        while True:
            result = self.recv_message()
            if result:
                return result

    # 2つのメッセージを送る(対象と命令または変更値)
    def send_two_message(self, type : str, message : str):
        print("QueueManager.py send_two_message : send message")
        self.send_message(type)
        self.send_message(message)
    