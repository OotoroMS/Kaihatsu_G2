import queue
import threading
import csv
# デバック用
import time
# シリアル通信
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
# キュー管理
from MEINTENANCE.QUEUE.QueueManager import QueueManager
# 定数
from MEINTENANCE.CONSTANTS.operation_status import *
from MEINTENANCE.CONSTANTS.command_type     import *
from MEINTENANCE.CONSTANTS.pless_command    import *
from MEINTENANCE.GUI.constants.file_path    import *
# データベース
from DATABASE.SQLCommunication  import SQLCommunication
SUCCESS = "SUCCESS"
PASS_QUERY = "UPDATE pass_num SET num = "
DELETE_QUERY = "DELETE FROM %s"
SELECT_QUERY = "SELECT * FROM %s"
TARGETTABLE = [
    "db_now",
    "db_countlog",
    "db_timelog",
    "db_sizelog"
]

class BackEndManager:
    def __init__(self, send_que : queue.Queue, recv_que : queue.Queue, send_lock : threading.Lock, recv_rock : threading.Lock, serial : SerialUIBridge) -> None:
        # キュー管理クラス
        self.queue_manager = QueueManager(send_que, recv_que, send_lock, recv_rock)
        # 稼働状況保持用
        self.operation = (OPERATION_STOP, "投入部")
        # ループフラグ
        self.running = True
        # シリアル通信クラス
        self.serial  = serial
        # デバック用
        self.timer  = 0
        self.op_flg = False
        # データベース
        self.db = SQLCommunication()
        self.db.set_db_name(DATABESE)
    
    def run(self):
        while self.running:
            self.serial.read_loop()
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
        result = self.serial.process_serial_queue()
        # 稼働状況
        if result[0] != None:
            if result[0][0] == OPERATION_ACTIVE or result[0][0] == OPERATION_STOP or result[0][0] == OPERATION_ERROR:
                self.operation = result[0]
        # デバック用
        # if self.op_flg:
        #     if self.operation == OPERATION_ACTIVE:
        #         self.operation = OPERATION_STOP
        #     elif self.operation == OPERATION_STOP:
        #         self.operation = OPERATION_ERROR
        #     elif self.operation == OPERATION_ERROR:
        #         self.operation = OPERATION_ACTIVE
        #     self.op_flg = False
        
    
    def plc_push_command(self):
        key = self.queue_manager.until_recv_message()
        if key:
            command = PUSH_COMMAND[key]
            # PLCに動作命令を出す
            print("BackEndManager.py plc_push_command : send to ", command)
            self.serial.send_set(command)
            self.timer = 0
            # PLCから完了命令が来るまで待機する
            while 1:
                message = self.serial.process_serial_queue()
                if message[0] != None:
                    if message[0][0] == "動作完了":
                        break
            time.sleep(1)
            self.queue_manager.send_message(message)

    def plc_hold_down_start_command(self):
        key = self.queue_manager.until_recv_message()
        if key:
            command = HOLD_DOWN_COMMAND[key]
            # PLCに動作命令を出す
            self.serial.send_set(command)
            print("BackEndManager.py plc_hold_down_start_command : PLC command is ", command)
            # 動作を始めたことを表示部に送る
            # print("BackEndManager.py plc_hold_down_start_command : Hold down is start")
            self.queue_manager.send_message(SUCCESS)

    def plc_hold_down_command(self):
        # PLCからの送信結果を受け取る
        message = RUN
        message = self.serial.process_serial_queue()
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
        self.serial.send_set("動作終了命令")
        print("BackEndManager.py plc_hold_down_end_command : Hold down is end.")
        self.queue_manager.send_message(SUCCESS)

    def plc_adsorption_command(self):
        message = self.queue_manager.until_recv_message()
        command = ADSORPTION_COMMAND[message]
        # コマンドをPLCに送信
        print(command)
        self.serial.send_set(command)
        print("BackEndManager.py plc_adsorption_command : Send to PLC is ", command)
        self.queue_manager.send_message(SUCCESS)

    def password_command(self):
        new_password = self.queue_manager.until_recv_message()
        if new_password:
            query = PASS_QUERY + str(new_password)
            self.db.db_query_execution(query=query)
            # print("new password is ", new_password)
            self.queue_manager.send_message(SUCCESS)

    def app_end_command(self):
        self.running = False
        self.queue_manager.send_message(APP_END)
    
    def db_reset_command(self):
        # データベース初期化処理を記述
        self.create_csv()
        for table in TARGETTABLE:
            delete_query = DELETE_QUERY % table
            print(delete_query)
            # print("変更前")
            # self.db.table_data_list_display(table_name=table)
            # self.db.db_query_execution(query=delete_query)
            # print("変更後")
            # self.db.table_data_list_display(table_name=table)
        time.sleep(2)
        self.queue_manager.send_message(SUCCESS)
    
    def send_operation_status(self):
        self.queue_manager.send_message(self.operation)
        # デバック用
        # self.op_flg = True
        # self.queue_manager.send_message([self.operation, "投入部"])

    def create_csv(self):
        with open(CSV_FILE_PATH, "w") as f:
            writer=csv.writer(f)
            for table in TARGETTABLE:
                query = SELECT_QUERY % table
                result = self.db.db_query_execution(query=query)
                writer.writerow([table + ' ----------------------------------------------------------------------'])
                for j in result:
                    j_list = list(j)
                    for k in range(len(j_list)):
                        if type(j_list[k]) is int:
                            j_list[k] = str(j_list[k])
                        elif j_list[k] is None:
                            j_list[k] = ""
                        elif type(j_list[k]) is float:
                            j_list[k] = str(j_list[k])
                    writer.writerow(list(j_list))