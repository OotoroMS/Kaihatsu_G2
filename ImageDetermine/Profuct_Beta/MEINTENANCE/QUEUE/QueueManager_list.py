# キューの管理を行うクラス
# キューによるデータの送信及び受信を行う
import queue
import threading
# 定数
from MEINTENANCE.CONSTANTS.pless_command    import *
from MEINTENANCE.CONSTANTS.command_type     import *
from MEINTENANCE.CONSTANTS.serial_result    import *
import MEINTENANCE.CONSTANTS.que_index      as que_index

class QueueManager:
    def __init__(self, plc_cmnd_que_list : list, plc_cmd_thread_lock_list : list, work_cmd_que_list : list,work_cmd_thread_lock_list : list, operation_que_list: list, operation_thread_lock_list : list) -> None:
        # キューリスト
        self.plc_cmd_que_list   = plc_cmnd_que_list
        self.work_cmd_que_list  = work_cmd_que_list
        self.operation_que_list = operation_que_list
        # スレッドロック
        self.plc_cmd_thread_lock_list   = plc_cmd_thread_lock_list
        self.work_cmd_thread_lock_list  = work_cmd_thread_lock_list
        self.operation_thread_lock_list = operation_thread_lock_list

    # 送信(汎用)
    def send_message(self, message, send_que : queue.Queue, send_lock : threading.Lock):
        with send_lock:
            send_que.put(message)
    
    # 受信(汎用)
    def recv_message(self, recv_que : queue.Queue, recv_lock : threading.Lock):
        if not recv_que.empty():
            with recv_lock:
                # print("QueueManager.py recv_message : get messsage")
                return recv_que.get()
        return ""
    
    # 何か受信するまで繰り返す
    def until_recv_message(self, recv_que : queue.Queue, recv_lock : threading.Lock):
        while True:
            result = self.recv_message(recv_que, recv_lock)
            if result:
                return result
    
    def hold_mode_recv_message(self):
        return self.recv_message(self.plc_cmd_que_list[que_index.PLC_RECV_QUEUE_INDEX], self.plc_cmd_thread_lock_list[que_index.PLC_RECV_THREAD_LOCK_INDEX])

    # PLCへのコマンドを送信
    def send_plc_command(self, message : str):
        self.send_message(message, self.plc_cmd_que_list[que_index.PLC_SEND_QUEUE_INDEX], self.plc_cmd_thread_lock_list[que_index.PLC_SEND_THREAD_LOCK_INDEX])
    
    # PLCへのコマンドを受け取る
    def recv_plc_command(self):
        return self.until_recv_message(self.plc_cmd_que_list[que_index.PLC_RECV_QUEUE_INDEX], self.plc_cmd_thread_lock_list[que_index.PLC_RECV_THREAD_LOCK_INDEX])

    # 作業検知キューへのコマンドを送信
    def send_work_command(self, message : str):
        self.send_message(message, self.work_cmd_que_list[que_index.WORK_SEND_QUEUE_INDEX], self.work_cmd_thread_lock_list[que_index.WORK_SEND_THREAD_LOCK_INDEX])
    
    def recv_work_command(self):
        return self.until_recv_message(self.work_cmd_que_list[que_index.WORK_RECV_QUEUE_INDEX], self.work_cmd_thread_lock_list[que_index.WORK_RECV_THREAD_LOCK_INDEX])
    
    # 稼働状況キューへのコマンドを送信
    def send_operation_command(self, message : str):
        self.send_message(message, self.operation_que_list[que_index.OPERATION_SEND_QUEUE_INDEX], self.operation_thread_lock_list[que_index.OPERATION_SEND_THREAD_LOCK_INDEX])
    
    def recv_operation_command(self):
        return self.until_recv_message(self.operation_que_list[que_index.OPERATION_RECV_QUEUE_INDEX], self.operation_thread_lock_list[que_index.OPERATION_RECV_THREAD_LOCK_INDEX])

    # 2つのメッセージを送る(対象と命令または変更値)
    def send_two_message(self, type : str, message : str):
        print("QueueManager.py send_two_message : send message")
        self.send_plc_command(type)
        self.send_plc_command(message)
    