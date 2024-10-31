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

WAIT_TIME = 0.01


class SerialManager:
    def __init__(self, serial_params: dict, queues: dict):
        """
        シリアル通信、キューマネージャー、および初期フラグの設定を行う。

        引数:
            serial_params (dict): シリアル通信のパラメータ（ポート、ボーレート、パリティなど）
            queues (dict): 送信および受信用のキュー辞書
        """
        # 各クラスのインスタンス化
        self.queue_manager = QueueManager(queues)
        self.serial_comm = SerialCommunicator(**serial_params)
        # ながいので変数に格納しておく
        self.send_queue = self.queue_manager.send_queue
        self.rcv_queue = self.queue_manager.receive_queue
        # 各フラグを初期化
        self.shutdown_flag: bool = SHUTDOWN_STATUS["active"]
        self.wait_for_response: bool = RESPONSE_STATUS["not_waiting"]

    def process_send_data(self) -> None:
        """
        送信処理のメインループ。終了フラグが立つまでキューからデータを取得し、シリアル通信で送信。

        戻り値:
            None
        """
        while self.shutdown_flag:
            try:                
                # 応答待ちの間は送信ができないようになっている
                if self.serial_comm.is_open and self.wait_for_response:
                    self.send_data_and_process()
                time.sleep(WAIT_TIME)
            except Exception as e:
                print(f"Send unexpected error: {e}")

    def send_data_and_process(self) -> None:
        """
        キューからデータを取得し、フォーマット後にシリアル送信。

        戻り値:
            None
        """
        byte = self.retrieve_data_from_queue()
        # byteに入るのはキューの中身かNoneの2択
        if byte:
            formatted_data = self.format_data_for_send(byte)
            self.send_formatted_data(formatted_data)

    def retrieve_data_from_queue(self) -> Optional[bytes]:
        """
        送信キューからデータを取得。データがない場合は None を返す。

        戻り値:
            Optional[bytes]: キューから取得したデータ（存在しない場合 None）
        """
        queue_item = self.queue_manager.send_queue_item()
        if queue_item:
            self.queue_manager.put_in_queue(self.send_queue, queue_item)
        return queue_item

    def format_data_for_send(self, byte: bytes) -> bytes:
        """
        送信データをフォーマットする。

        引数:
            byte (bytes): キューから取得したデータ

        戻り値:
            bytes: フォーマットされたデータ
        """
        format_data = self.format_send(byte)  # データをフォーマット
        return format_data

    def send_formatted_data(self, data: bytes) -> None:
        """
        フォーマット済みデータをシリアル通信で送信。

        引数:
            data (bytes): 送信するデータ
        """
        self.serial_comm.serial_write(data)  # シリアルポートにデータを書き込む
        self.wait_for_response = RESPONSE_STATUS["waiting"]  # レスポンス待機を有効化

    def process_received_data(self) -> None:
        """
        受信処理のメインループ。終了フラグが立つまでシリアルポートからデータを受信。

        戻り値:
            None
        """
        while self.shutdown_flag:
            try:
                if self.serial_comm.is_open:  # シリアルポートがオープンであればデータを受信
                    self.receive_data_and_process()
                time.sleep(WAIT_TIME)  # 一定の待機時間を設ける
            except Exception as e:
                print(f"Receive unexpected error: {e}")

    def receive_data_and_process(self) -> None:
        """
        受信データを取得し、比較処理を実行。

        戻り値:
            None
        """
        data = self.serial_comm.serial_read()  # シリアルポートからデータを受信
        self.compare_recive_data(data)  # 受信データを比較

    def compare_recive_data(self, data: bytes) -> None:
        """
        受信データの接頭語に基づき処理を分岐。

        引数:
            data (bytes): 受信したデータ
        """
        if data.startswith(DATA_PREFIX["data_in"]):  # データが特定の接頭語で始まる場合
            print("Received data")
            self.queue_manager.put_in_queue(self.rcv_queue, data[FARST:LAST])  # 受信データを受信キューに追加
            self.send_response(data[FARST:LAST])  # レスポンスを送信
        elif data.startswith(DATA_PREFIX["ack"]):  # ACKデータが受信された場合
            print("Response data")
            self.compare_data(data)  # 受信したデータを比較

    def send_response(self, response_data: bytes) -> None:
        """
        レスポンスデータを送信する。フォーマット後にシリアル送信。

        引数:
            response_data (bytes): レスポンスデータ
        """
        response = DATA_PREFIX["ack"] + response_data + LINE_ENDING  # レスポンスのフォーマット
        self.serial_comm.serial_write(response)  # シリアルポートにレスポンスを書き込む

    def compare_data(self, data: bytes) -> None:
        """
        受信データと送信キュー内データを比較し、一致しない場合は再送信。

        引数:
            data (bytes): 受信データ
        """
        send_data = self.queue_manager.get_from_queue(self.send_queue)  # 送信キューからデータを取得
        if data[FARST:LAST] == send_data:  # データが一致するか確認
            print("Data matches")
        else:  # 一致しない場合は再送信
            print("Data does not match, resending")
            self.queue_manager.put_in_queue(self.send_queue, data)  # 受信データを再送信キューに追加
        self.wait_for_response = RESPONSE_STATUS["not_waiting"]  # レスポンス待機を無効化

    def format_send(self, byte: bytes) -> Optional[bytes]:
        """
        送信データをフォーマットし、接頭語と改行コードを付与。

        引数:
            byte (bytes): 送信するバイトデータ

        戻り値:
            Optional[bytes]: フォーマット済みデータ（失敗時 None）
        """
        if byte:  # バイトデータが存在する場合
            format_byte = DATA_PREFIX["data_in"] + byte + LINE_ENDING  # 接頭語と改行コードを付与
            return format_byte
        else:
            return None  # データがない場合は None を返す

    def end(self) -> None:
        """
        終了処理を実行し、送受信ループを停止後シリアル接続を閉じる。

        戻り値:
            None
        """
        self.shutdown_flag = SHUTDOWN_STATUS["inactive"]  # 終了フラグを立てる
        self.serial_comm.serial_close()  # シリアルポートを閉じる
