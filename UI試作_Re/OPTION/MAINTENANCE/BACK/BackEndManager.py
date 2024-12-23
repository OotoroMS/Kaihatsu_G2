import queue
import threading
# デバック用
import time
# シリアル通信
# from SERIAL.do_serial   import DoSerial
# キュー管理
from QUEUE.QueueManager import QueueManager
# 定数
from CONSTANTS.operation_status import *
from CONSTANTS.command_type     import *
from CONSTANTS.pless_command    import *

SUCCESS = "SUCCESS"

class BackEndManager:
    def __init__(self, send_que : queue.Queue, recv_que : queue.Queue, send_lock : threading.Lock, recv_rock : threading.Lock) -> None:
        # キュー管理クラス
        self.queue_manager = QueueManager(send_que, recv_que, send_lock, recv_rock)
        # 稼働状況保持用
        self.operation = OPERATION_ERROR
        # ループフラグ
        self.running = True
        # デバック用
        self.timer  = 0
        self.op_flg = False
    
    def run(self):
        while self.running:
            self.receive_ui()
            self.recv_plc()
    
    def receive_ui(self):
        command_type = self.queue_manager.recv_message()
        # if command_type:
        #     print("BackEndManager.py run : command_type is ", command_type)
        if command_type == PLC:
            self.plc_push_command()
        elif command_type == HOLD_DOWN_START:
            self.plc_hold_down_start_command()
        elif command_type == HOLD_DOWN_END:
            self.plc_hold_down_end_command()
        elif command_type == PASSWORD:
            self.password_command()
        elif command_type == DB_RESET:
            self.db_reset_command()
        elif command_type == APP_END:
            self.app_end_command()
        elif command_type == ADSORPTION:
            self.plc_adsorption_command()
        elif command_type == HOLD_DOWN:
            self.plc_hold_down_command()
        elif command_type == OPERATION_STATUS:
            self.send_operation_status()

    def recv_plc(self):
        # PLCからの通信を受け取る
        # 結果を識別
        # 稼働状況を試す
        if self.op_flg:
            if self.operation == OPERATION_ACTIVE:
                self.operation = OPERATION_STOP
            elif self.operation == OPERATION_STOP:
                self.operation = OPERATION_ERROR
            elif self.operation == OPERATION_ERROR:
                self.operation = OPERATION_ACTIVE
            self.op_flg = False
        
    
    def plc_push_command(self):
        key = self.queue_manager.until_recv_message()
        if key:
            command = PUSH_COMMAND[key]
            # PLCに動作命令を出す
            print("BackEndManager.py plc_push_command : send to ", command)
            self.timer = 0
            # PLCから完了命令が来るまで待機する
            time.sleep(1)
            self.queue_manager.send_message(["正常", "移動部"])

    def plc_hold_down_start_command(self):
        key = self.queue_manager.until_recv_message()
        if key:
            command = HOLD_DOWN_COMMAND[key]
            # PLCに動作命令を出す
            print("BackEndManager.py plc_hold_down_start_command : PLC command is ", command)
            # 動作を始めたことを表示部に送る
            # print("BackEndManager.py plc_hold_down_start_command : Hold down is start")
            self.queue_manager.send_message(SUCCESS)

    def plc_hold_down_command(self):
        # PLCからの送信結果を受け取る
        message = RUN
        # デバック用
        if self.timer >= 8:
                    self.timer = 0
                    message    = FINISH
        # ｾﾝｻが反応しなければ
        else:
            self.timer += 1
        if message == FINISH:
            self.queue_manager.send_message(message)
        elif self.queue_manager.send_que.empty():
            self.queue_manager.send_message(message)

    def plc_hold_down_end_command(self):
        # PLCに動作終了命令を出す
        print("BackEndManager.py plc_hold_down_end_command : Hold down is end.")
        self.queue_manager.send_message(SUCCESS)

    def plc_adsorption_command(self):
        message = self.queue_manager.until_recv_message()
        command = ADSORPTION_COMMAND[message]
        # コマンドをPLCに送信
        print("BackEndManager.py plc_adsorption_command : Send to PLC is ", command)
        self.queue_manager.send_message(SUCCESS)

    def password_command(self):
        new_password = self.queue_manager.until_recv_message()
        if new_password:
            # print("new password is ", new_password)
            self.queue_manager.send_message(SUCCESS)

    def app_end_command(self):
        self.running = False
        self.queue_manager.send_message(APP_END)
    
    def db_reset_command(self):
        # データベース初期化処理を記述
        time.sleep(2)
        self.queue_manager.send_message(SUCCESS)
    
    def send_operation_status(self):
        # デバック用
        self.op_flg = True
        self.queue_manager.send_message([self.operation, "投入部"])