import time
from queue import Queue
from serial_data_formatter import SerialDataFormatter
from serial_communicator import SerialCommunicator
from queue_manager import QueueManager

class SerialConnection:
    def __init__(self, serial_params: dict, queues: dict):
        """
        初期化メソッド。シリアル通信、キューマネージャー、およびデータフォーマッターを設定。

        引数:
            serial_params (dict): シリアル通信のパラメータ（ポート、ボーレート、パリティなど）
            queues (dict): キューの辞書（送信・受信用）
        """
        self.queue_manager = QueueManager(queues)
        self.data_formatter = SerialDataFormatter()
        self.serial_comm = SerialCommunicator(**serial_params)
        self.shutdown_flag: bool = False  # 通信終了フラグ
        self.wait_for_response: bool = False  # レスポンス待機中フラグ

    def process_send_data(self) -> None:
        """
        送信処理を行うメインループ。shutdown_flag が立つまで、キューからデータを取得し、
        シリアル通信で送信する。
        """
        while not self.shutdown_flag:
            try:
                if self.serial_comm.is_open and not self.wait_for_response:
                    self.send_data_and_process()
                time.sleep(0.01)  # 待機時間
            except Exception as e:
                print(f"Send unexpected error: {e}")

    def send_data_and_process(self) -> None:
        """
        送信キューからデータを取得し、シリアル送信処理を行う。データをバイト形式に変換し、
        フォーマット後に送信する。
        """
        byte = self.queue_manager.send_queue_item()
        if byte is not None:
            self.queue_manager.put_in_queue(self.queue_manager.send_queue, byte)
            data = self.data_formatter.format_send(byte)
            self.serial_comm.write(data)
            self.wait_for_response = True  # レスポンス待機に設定

    def process_received_data(self) -> None:
        """
        受信処理を行うメインループ。shutdown_flag が立つまでシリアルポートからデータを受信し、
        処理を行う。
        """
        while not self.shutdown_flag:
            try:
                if self.serial_comm.is_open:
                    self.receive_data_and_process()
                time.sleep(0.01)  # 待機時間
            except Exception as e:
                print(f"Receive unexpected error: {e}")

    def receive_data_and_process(self) -> None:
        """
        シリアルポートからデータを受信し、受信データの比較処理を行う。
        """
        data = self.serial_comm.read()
        self.compare_recive_data(data)

    def compare_recive_data(self, data: bytes) -> None:
        """
        受信したデータの先頭バイトに基づき、処理を分岐する。

        引数:
            data (bytes): 受信データ
        """
        if data.startswith(b'\x00\x01'):
            print("Received data")
            self.queue_manager.put_in_queue(self.queue_manager.receive_queue, data[2:3])
            self.send_response(data[2:3])
        elif data.startswith(b'\x00\x02'):
            print("Response data")
            self.compare_data(data)

    def send_response(self, response_data: bytes) -> None:
        """
        レスポンスデータを送信する。レスポンスフォーマットを整え、シリアルポート経由で送信。

        引数:
            response_data (bytes): 送信するレスポンスデータ
        """
        response = b'\x00\x02' + response_data + b'\r\n'
        self.serial_comm.write(response)

    def compare_data(self, data: bytes) -> None:
        """
        受信データと送信キュー内のデータを比較する。データが一致しない場合、再送信を行う。

        引数:
            data (bytes): 受信データ
        """
        send_data = self.queue_manager.get_from_queue(self.queue_manager.send_queue)
        if data[2:3] == send_data:
            print("Data matches")
        else:
            print("Data does not match, resending")
            self.queue_manager.put_in_queue(self.queue_manager.send_queue, data)
        self.wait_for_response = False  # 応答待ちを解除d

    def end(self) -> None:
        """
        接続終了処理を行う。shutdown_flag を立てて送受信ループを終了し、シリアルポートを閉じる。
        """
        self.shutdown_flag = True
        self.serial_comm.close()
