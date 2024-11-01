import time
from queue import Queue
from serial_communicator import SerialCommunicator
from queue_manager import QueueManager
from typing import Optional

FARST = 2
LAST = 3

SHUTDOWN_STATUS = {
    "active": True,
    "inactive": False
}

RESPONSE_STATUS = {
    "not_waiting": True,
    "waiting": False
}

DATA_PREFIX = {
    "ack": b'\x00\x02',
    "data_in": b'\x00\x01'
}

LINE_ENDING = b'\r\n'

# 引数:
#    serial_params (dict): シリアル通信のパラメータ（ポート、ボーレートなど）
#    queues (dict): 送信および受信操作用のキューの辞書
class SerialManager:
    def __init__(self, serial_params: dict, queues: dict):
        self.queue_manager = QueueManager(queues)
        self.serial_comm = SerialCommunicator(**serial_params)                
        self.shutdown_flag: bool = self.isshutdown("active")
        self.wait_for_response: bool = self.isresponse("not_waiting")

    # データ送信のメインループ。キューからデータを取得し、条件を満たす場合にシリアルで送信する。
    # 戻り値: None
    def process_send_data(self) -> None:
        is_open = self.serial_comm.is_open
        while self.shutdown_flag:
            try:
                if is_open and self.wait_for_response:
                    self.send_data_and_process()
            except Exception as e:
                print(f"Send unexpected error: {e}")

    # データ受信のメインループ。shutdownフラグがアクティブな間、シリアルからデータを受信し処理する。
    # 戻り値: None
    def process_received_data(self) -> None:
        is_open = self.serial_comm.is_open
        while self.shutdown_flag:
            try:
                if is_open:
                    self.receive_data_and_process()
            except Exception as e:
                print(f"Receive unexpected error: {e}")
    
    # 送信および受信ループを終了し、シリアル接続を閉じる。
    # 戻り値: None
    def end(self) -> None:
        self.shutdown_flag = self.isshutdown("inactive")
        self.serial_comm.serial_close()

    # キューからデータを取得し、フォーマットしてシリアルで送信する。
    # 戻り値: None
    def send_data_and_process(self) -> None:
        queue_item = self.retrieve_data_from_queue()
        if queue_item:
            formatted_data = self.format_data_for_send(queue_item)
            self.send_formatted_data(formatted_data)

    # 送信キューからデータを取得する。データがない場合はNoneを返す。
    # 戻り値: Optional[bytes]: キューから取得したデータ、またはキューが空の場合はNone。
    def retrieve_data_from_queue(self) -> Optional[bytes]:
        send_queue = self.queue_manager.send_queue
        queue_item = self.queue_manager.send_queue_item()
        if queue_item:
            self.queue_manager.put_in_queue(send_queue, queue_item)
        return queue_item

    # 送信データをフォーマットするため、接頭辞と行末を追加する。
    # 引数: byte (bytes): フォーマットするバイトデータ
    # 戻り値: bytes: フォーマット済みデータ
    def format_data_for_send(self, byte: bytes) -> bytes:
        data_prefix = DATA_PREFIX["data_in"]
        line_ending = LINE_ENDING
        formatted_data = data_prefix + byte + line_ending
        return formatted_data

    # フォーマット済みのデータをシリアルで送信し、応答待機フラグを設定する。
    # 引数: data (bytes): 送信するフォーマット済みデータ
    # 戻り値: None
    def send_formatted_data(self, data: bytes) -> None:
        self.serial_comm.serial_write(data)
        self.wait_for_response = self.isresponse("waiting")

    # シリアルからデータを受信し、定義されたロジックに従って処理する。
    # 戻り値: None
    def receive_data_and_process(self) -> None:
        data = self.serial_comm.serial_read()
        self.compare_receive_data(data)

    # 受信したデータを比較し、定義された接頭辞に基づいて処理する。
    # 引数: data (bytes): 比較する受信データ
    # 戻り値: None
    def compare_receive_data(self, data: bytes) -> None:
        rcv_queue = self.queue_manager.receive_queue
        data_prefix_data_in = DATA_PREFIX["data_in"]
        data_prefix_ack = DATA_PREFIX["ack"]
        
        if data.startswith(data_prefix_data_in):
            print("データを受信しました")
            self.queue_manager.put_in_queue(rcv_queue, data[FARST:LAST])
            self.send_response(data[FARST:LAST])
        elif data.startswith(data_prefix_ack):
            print("応答データ")
            self.compare_data(data)

    # 接頭辞でフォーマットされた応答を送信する。
    # 引数: response_data (bytes): フォーマットして送信する応答データ
    # 戻り値: None
    def send_response(self, response_data: bytes) -> None:
        formatted_response = self.format_byte(response_data, "ack")
        if formatted_response:
            self.serial_comm.serial_write(formatted_response)

    # 受信データを送信データと比較し、必要に応じて再送信する。
    # 引数: data (bytes): 比較する受信データ
    # 戻り値: None
    def compare_data(self, data: bytes) -> None:
        send_queue = self.queue_manager.send_queue
        send_data = self.queue_manager.get_from_queue(send_queue)
        if data[FARST:LAST] == send_data:
            print("データが一致しました")
        else:
            print("データが一致しないため、再送信します")
            self.queue_manager.put_in_queue(send_queue, data)
        self.wait_for_response = self.isresponse("not_waiting")

    # 指定された接頭辞と行末でバイト列をフォーマットする。
    # 引数: byte (bytes): フォーマットするバイト列
    #       msg (str): 使用する接頭辞を示すキー
    # 戻り値: Optional[bytes]: フォーマットされたバイト列、フォーマットに失敗した場合はNone
    def format_byte(self, byte: bytes, msg: str) -> Optional[bytes]:
        prefix = DATA_PREFIX.get(msg)
        if prefix and byte:
            return prefix + byte + LINE_ENDING
        return None
        
    # キーに基づいてシャットダウン状態を取得する。
    # 引数: msg (str): シャットダウン状態を取得するキー
    # 戻り値: bool: シャットダウン状態
    def isshutdown(self, msg: str) -> bool:
        return SHUTDOWN_STATUS.get(msg, False)
    
    # キーに基づいて応答状態を取得する。
    # 引数: msg (str): 応答状態を取得するキー
    # 戻り値: bool: 応答状態
    def isresponse(self, msg: str) -> bool:
        return RESPONSE_STATUS.get(msg, False)
