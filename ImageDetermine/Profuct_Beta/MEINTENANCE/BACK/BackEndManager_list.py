import queue
import threading
import csv
# デバック用
import time
# シリアル通信
from SERIAL.manager.SerialUIBridge  import SerialUIBridge
import SERIAL.dict.plc_cmd as cmd
import SERIAL.dict.normal as nomal
# キュー管理
from MEINTENANCE.QUEUE.QueueManager_list import QueueManager
# 定数
from MEINTENANCE.CONSTANTS.operation_status  import *
from MEINTENANCE.CONSTANTS.command_type      import *
from MEINTENANCE.CONSTANTS.pless_command     import *
from MEINTENANCE.GUI.constants.file_path     import *
from MEINTENANCE.CONSTANTS.ui_plc_pc_command import *
import MEINTENANCE.CONSTANTS.move_moter_pos  as motor_pos
# データベース
from DATABASE.SQLCommunication  import SQLCommunication
MEINTENANCE = ("メンテナンス", "動作確認")
STEPING_COMAND = ("20ステップ", "外観検査部")
MAIN = ("主動作", "動作確認")
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
    def __init__(self, plc_cmd_que_list : list, plc_cmd_thred_lock : list, work_cmd_que_list : list, work_cmd_thred_lock: list, operation_que_list : list, operation_thread_lock : list, serial : SerialUIBridge) -> None:
        # キュー管理クラス
        self.queue_manager = QueueManager(plc_cmd_que_list, plc_cmd_thred_lock, work_cmd_que_list, work_cmd_thred_lock, operation_que_list, operation_thread_lock)
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
    
    #　メッセージを送る
    def send_message(self, message):
        if message in cmd.comand:
            send_message = cmd.comand[message]
            self.serial.serial_write(send_message)
            print("BackEndManager.py send_message : Send message is ", send_message)


    # 受信メッセージを受け取る
    def recv_message(self, comparruson_source):
        while 1:
            if not self.serial.rcv_queue.empty():
                message = self.serial.rcv_queue.get()
                print("BackEndManager.py recv_message : message is ", message)
                if self.juge_message(message, comparruson_source):
                    return nomal.comand[message]
    
    # メッセージが正しいか判定
    def juge_message(self, message, comparruson_source):
        if message in nomal.comand:
            result = nomal.comand[message]
            print("BackEndManager.py juge_message : result is ", result)
            print("BackEndManager.py juge_message : comparruson_source is ", comparruson_source)
            if result[0] == comparruson_source[0] and result[1] == comparruson_source[1]:
                return True
        return False

    def run(self):
        # PLCに動作確認に移行するコマンドを送る
        self.send_message(MEINTENANCE)
        self.recv_message(MODE_MEINTENANCE)
        # # メインループ
        while self.running:
            # self.serial.read_loop()
            self.receive_ui()
            self.recv_plc()
        # 主動作モード移行時の処理
        self.send_message(MAIN)
        self.recv_message(MODE_MAIN)
        print("BackEndManager.py run : end")
    
    def receive_ui(self):
        command_type = self.queue_manager.recv_plc_command()
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
        elif command_type == LIGHT:
            self.plc_light_command()
        elif command_type == HOLD_DOWN:
            self.plc_hold_down_command()
        elif command_type == OPERATION_STATUS:
            self.send_operation_status()
        elif command_type == WORK_STATUS:
            self.send_work_status()

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
        print("BackEndManager.py plc_push_command : Start")
        key = self.queue_manager.recv_plc_command()
        if key:
            print("BackEndManager.py plc_push_command : key is ", key)
            if key in PUSH_COMMAND:
                command = PUSH_COMMAND[key]
                self.send_message(command)
                result = PUSH_RESULT[key]
            if key == STEPING:
                self.recv_message(MOTOR_ON)
                self.send_message(STEPING_COMAND)
                print("BackEndManager.py plc_push_command : Send to message")

            # PLCから完了命令が来るまで待機する
            
            message = self.recv_message(result)
            time.sleep(1)
            message = ("動作完了", "動作確認")
            self.queue_manager.send_plc_command(message)
        else:
            print("BackEndManager.py plc_push_command : key is None")
        print("BackEndManager.py plc_push_command : End")

    def plc_hold_down_start_command(self):
        key = self.queue_manager.recv_plc_command()
        if key in HOLD_DOWN_COMMAND:
            command = HOLD_DOWN_COMMAND[key]
            # PLCに動作命令を出す
            self.send_message(command)
            print("BackEndManager.py plc_hold_down_start_command : PLC command is ", command)
            # 動作を始めたことを表示部に送る
            print("BackEndManager.py plc_hold_down_start_command : Hold down is start")
            self.queue_manager.send_plc_command(SUCCESS)
            self.queue_manager.send_plc_command(self.serial.get_move_pos())

    def plc_hold_down_command(self):
        # PLCからの送信結果を受け取る
        # if self.serial.rcv_queue.empty():
        #     message = None
        # else:
        #     message = self.serial.rcv_queue.get()
        message = self.serial.get_move_pos()
        # print("BackEndManager.py plc_hold_down_command : message is ", message)
        # 受信結果を判別
        if message in motor_pos.MOTOR_POS_LIST:
            self.queue_manager.send_plc_command(message)
        # # デバック用
        # if self.timer >= 8:
        #             self.timer = 0
        #             message    = FINISH
        # ｾﾝｻが反応しなければ
        # else:
        #     self.timer += 1
        # if message == FINISH:
        #     self.queue_manager.send_message(message)
        # elif self.queue_manager.send_que.empty():
        #     self.queue_manager.send_message(message)

    def plc_hold_down_end_command(self):
        # PLCに動作終了命令を出す
        # self.send_message(HOLD_DOWN_COMMAND[HOLD_END])
        self.send_message(("移動用モータ停止コマンド", "移載部"))
        print("BackEndManager.py plc_hold_down_end_command : Hold down is end.")
        pos = self.serial.get_move_pos()
        # self.queue_manager.send_plc_command(pos)
        # 動作終了を表示部に送る
        self.queue_manager.send_plc_command(SUCCESS)

    def plc_adsorption_command(self):
        message = self.queue_manager.recv_plc_command()
        print("BackEndManager.py plc_adsorption_command : message is ", message)
        cmd_key = ADSORPTION_COMMAND[message]
        # コマンドをPLCに送信
        print("BackEndManager.py plc_adsorption_command : cmd_key is ", cmd_key)
        self.send_message(cmd_key)
        # 実行結果を受けとる
        result = ADSORPTION_RESULT[message]
        self.recv_message(result)
        
        self.queue_manager.send_plc_command(SUCCESS)
    
    def plc_light_command(self):
        message = self.queue_manager.recv_plc_command()
        print("BackEndManager.py plc_light_command : message is ", message)
        cmd_key = LIGHT_COMMAND[message]
        # コマンドをPLCに送信
        print("BackEndManager.py plc_light_command : cmd_key is ", cmd_key)
        self.send_message(cmd_key)
        # 実行結果を受けとる
        result = LIGHT_RESULT[message]
        self.recv_message(result)
        
        self.queue_manager.send_plc_command(SUCCESS)

    def password_command(self):
        new_password = self.queue_manager.until_recv_message()
        if new_password:
            query = PASS_QUERY + str(new_password)
            self.db.db_query_execution(query=query)
            # print("new password is ", new_password)
            self.queue_manager.send_message(SUCCESS)

    def app_end_command(self):
        self.running = False
        self.queue_manager.send_plc_command(APP_END)
    
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
        self.queue_manager.send_operation_command(self.operation)
        # デバック用
        # self.op_flg = True
        # self.queue_manager.send_message([self.operation, "投入部"])
    
    def send_work_status(self):
        in_work = self.serial.in_work
        out_work = self.serial.out_work
        if in_work or out_work:
            self.queue_manager.send_work_command([in_work, out_work])


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