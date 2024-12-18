from typing import Optional, Tuple

from SERIAL.serial_communicator import SerialCommunicator
from SERIAL.type_check          import type_check_decorator  # type_check デコレーターをインポート

FARST = 2
LAST = 3

SHUTDOWN_STATUS = {
    "startup": True,
    "shutdown": False
}

RESPONSE_STATUS = {
    "not_waiting": True,
    "waiting": False
}

DATA_PREFIX = {
    "ack": b'\x02',
    "data_in": b'\x01'
}

LINE_ENDING = b'\n'

# SerialCommunicatorを継承したクラス
class SerialManager(SerialCommunicator):
    def __init__(self, serial_params: dict):
        # serial_paramsの型チェックを追加
        if not isinstance(serial_params, dict):
            raise TypeError("serial_params should be a dictionary")
        
        if not all(key in serial_params for key in ['port', 'baudrate', 'timeout']):
            raise ValueError("serial_params must contain 'port', 'baudrate', and 'timeout' keys")
        
        # 親クラスのコンストラクタを呼び出す
        super().__init__(**serial_params)
        
        self.is_shutdown: bool = SHUTDOWN_STATUS["startup"]
        self.is_response: bool = RESPONSE_STATUS["not_waiting"]
        self.send_data: bytes = b''

    # 受信関数    
    def serial_receive(self) -> tuple[bytes, bool]:
        if self.is_shutdown:
            try:
                rcv_data = super().log_serial_read()
                return rcv_data
            except Exception as e:
                print(f"Manager Receive unexpected error: {e}")
                return b'', False
    
    # 送信関数
    @type_check_decorator({'data': bytes})
    def serial_send(self, data: bytes):
        if self.is_shutdown:
            try:
                super().log_serial_write(data)                
            except Exception as e:
                print(f"{self.__class__.__name__}: {self.serial_send.__name__}:{e}")
    
    # 送信データの成形
    @type_check_decorator({'data':bytes, 'prefix':bytes})
    def format_bytes(self, data: bytes, prefix: bytes = DATA_PREFIX["data_in"]) -> bytes:
        converted_data = prefix + data + LINE_ENDING
        return converted_data
    
    # 応答を送信する関数
    @type_check_decorator({'data': bytes})
    def serial_response(self, data: bytes):
        if self.is_shutdown:
            try:
                super().log_serial_write(data)
            except Exception as e:
                print(f"Response unexpected error: {e}")
    
    # 受信データが応答か送信されたものか判別する関数
    @type_check_decorator({'data': bytes})
    def compare_receive(self, data: bytes) -> tuple[bytes, bytes]:
        prefix_request = DATA_PREFIX["data_in"]
        prefix_response = DATA_PREFIX["ack"]

        if data.startswith(prefix_request):
            print("PLCからの送信データだよ")
            return data, prefix_response

        elif data.startswith(prefix_response):
            print("PLCからの応答データだよ")
            return data, prefix_request

        else:
            print("よくわからないデータだよ")
            return b'', None

    # 受信データの判別結果から処理を行う関数
    @type_check_decorator({'data': bytes})
    def compare_and_process_receive(self, data: bytes) -> bytes:
        byte, prefix = self.compare_receive(data)

        if prefix == DATA_PREFIX["ack"]:
            # 応答を返すよ
            self.response(byte[2:3], prefix)
            # 識別子とデータの中身を渡すよ 
            return data[1:3]
            
        elif prefix == DATA_PREFIX["data_in"]:            
            # 応答待ちフラグを解除
            self.is_response = RESPONSE_STATUS["not_waiting"]
            # 合っているか判別するよ
            self.compare_send(data[2:3])
            return b''

        else:            
            # 応答待ちフラグは解除するよ
            self.is_response = RESPONSE_STATUS["not_waiting"]
            return b''

    # 応答を返す関数
    @type_check_decorator({'data': bytes, 'prefix': bytes})
    def response(self, data: bytes, prefix: bytes):
        # データの成形
        response_data = self.format_bytes(data, prefix)
        # データの送信(1回)
        self.serial_response(response_data)

    # データが一致しているか判別する
    @type_check_decorator({'data': bytes})
    def compare_send(self, data: bytes):
        if data == self.send_data[1:2]:
            print("OK。送信データと応答データが一致したよ")
        else:
            print("NG。送信データと応答データが不一致だったよ")
            # 再送させるよ
            self.send(data)

    # 送信の一連の動作を行う関数
    @type_check_decorator({'data': bytes})
    def send(self, data: bytes):
        if self.is_response:
            # データの成形
            request_data = self.format_bytes(data)
            # 判定用に保存
            self.send_data = request_data
            # データの送信(1回)
            self.serial_send(request_data)
            # 応答待ちに設定
            self.is_response = RESPONSE_STATUS["waiting"]

    # 受信の一連の動作を行う関数
    def receive(self) -> tuple[bytes, bool]:
        result = b'', True # 初期値設定
        rcv_data = self.serial_receive()
        # 受信データのbytes部分を渡す
        if rcv_data[0]:
            # 受信データの判別
            result[0] = self.compare_and_process_receive(rcv_data[0])
        return result

    # シリアル通信を終了する際使用する関数
    def serial_close(self):
        self.is_shutdown = SHUTDOWN_STATUS["shutdown"]
        try:
            super().serial_close()  # 親クラスのメソッドを呼び出し
        except Exception as e:
            print(f"Serial close unexpected error: {e}")
