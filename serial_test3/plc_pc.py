# plc_pc.py
from typing import Optional, Tuple

# 自作プログラムをimport
# いつもの
from type_check import type_check_decorator
import log_error
from Status     import ResponseStatus, ShutdownStatus, OperationStatus
from Format     import DataPrefix, LineEnding
# シリアル通信のクラス(このクラスの親)
from serial_communicator import SerialCommunicator

FARST = 2
LAST = 3

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
        
        self.is_shutdown: ShutdownStatus = ShutdownStatus.STARTUP
        self.is_response: ResponseStatus = ResponseStatus.NOT_WAITING
        self.send_data: bytes = b''

    # 受信関数    
    def serial_receive(self) -> tuple[bytes, OperationStatus]:
        if self.is_shutdown == ShutdownStatus.STARTUP:
            try:
                # シリアル通信の受信関数
                # rcv_dataの中身 tuple[bytes, OperationStatus]
                rcv_data, status = super().log_serial_read()
                return rcv_data, status
            except Exception as e:
                log_error(self, self.serial_receive.__name__, e)
                return b'' , OperationStatus.FAILURE
    
    # 送信関数
    @type_check_decorator({'data': bytes})
    def serial_send(self, data: bytes) -> OperationStatus:
        if self.is_shutdown == ShutdownStatus.STARTUP:
            try:
                # シリアル通信の送信関数
                # 引数(bytes)
                return super().log_serial_write(data)
            except Exception as e:
                log_error(self, self.serial_send.__name__, e)
                return OperationStatus.FAILURE
    
    # 送信データの成形
    @type_check_decorator({'data':bytes, 'prefix':DataPrefix})
    def format_bytes(self, data: bytes, 
                     prefix: DataPrefix = DataPrefix.DATA_IN) -> bytes:
        converted_data = prefix.value + data + LineEnding.LF.value
        # 返り値の例 b'\x01\x8e' , b'\x02\x8e'
        return converted_data
    
    # 応答を送信する関数
    @type_check_decorator({'data': bytes})
    def serial_response(self, data: bytes) -> OperationStatus:
        if self.is_shutdown == ShutdownStatus.STARTUP:
            try:
                return super().log_serial_write(data)
            except Exception as e:
                log_error(self, self.serial_response.__name__, e)
                return OperationStatus.FAILURE
    
    # 引数の値の接頭語で処理を分岐させるための関数
    @type_check_decorator({'data': bytes})
    def compare_receive(self, data: bytes) -> tuple[bytes, DataPrefix]:
        prefix_data_in = DataPrefix.DATA_IN
        prefix_ack = DataPrefix.ACK

        # 接頭語が b'\x01' だった場合
        if data.startswith(prefix_data_in.value):
            print("PLCからの送信データだよ")
            return data, prefix_ack

        # 接頭語が b'\x02' だった場合
        elif data.startswith(prefix_ack.value):
            print("PLCからの応答データだよ")
            return data, prefix_data_in

        # そのどちらでもない 場合
        else:
            print("よくわからないデータだよ")
            return b'', DataPrefix.NONE

    # 受信データの判別結果から処理を行う関数
    @type_check_decorator({'data': bytes})
    def compare_and_process_receive(self, data: bytes) -> bytes:
        # 受信データの接頭語をチェック
        byte, prefix = self.compare_receive(data)

        if prefix == DataPrefix.ACK:
            # データの本体。コマンドデータを切り出している
            cmd_data = byte[2:3]
            self.response(cmd_data, prefix)
            # これは判別データとコマンドデータを返している
            status_and_cmd_data = byte[1:3]
            return status_and_cmd_data
            
        elif prefix == DataPrefix.DATA_IN:            
            # 応答待ちフラグを解除
            self.is_response = ResponseStatus.NOT_WAITING
            # データの本体。コマンドデータを切り出している
            cmd_data = byte[2:3]
            self.compare_send(cmd_data)
            # 空のバイト列を返す
            return b''

        else:            
            # 応答待ちフラグは解除するよ
            self.is_response = ResponseStatus.NOT_WAITING
            # 空のバイト列を返す
            return b''

    # 応答を返す関数
    @type_check_decorator({'data': bytes, 'prefix': DataPrefix})
    def response(self, data: bytes, prefix: DataPrefix) -> OperationStatus:
        # データの成形 例 b'\x8e' , DataPrefix.ACK → b'\x02\x8e'
        response_data = self.format_bytes(data, prefix)
        # データの送信(1回)
        return self.serial_response(response_data)

    # データが一致しているか判別する
    @type_check_decorator({'data': bytes})
    def compare_send(self, data: bytes):
        # self.send_dataの例 b'\x01\x8e'
        # dataの例 b'\x8e'
        cmd_data = self.send_data[1:2]
        if data == cmd_data:
            print("OK。送信データと応答データが一致したよ")
        else:
            print("NG。送信データと応答データが不一致だったよ")
            # 再送させるよ
            self.send(data)

    # 送信の一連の動作を行う関数
    @type_check_decorator({'data': bytes})
    def send(self, data: bytes) -> OperationStatus:
        if self.is_response:
            # データの成形 例 b'\x8e' → b'\x01\x8e'
            request_data = self.format_bytes(data)
            # 判定用に保存 
            # self.send_dataはここ以外でinitでしか代入が行われてない
            self.send_data = request_data
            # データの送信
            result = self.serial_send(request_data)
            # 応答待ちに設定
            self.is_response = ResponseStatus.WAITING
            return result

    # 受信の一連の動作を行う関数
    def receive(self) -> tuple[bytes, OperationStatus]:
        result = b'', OperationStatus.FAILURE # 初期値設定
        # rcv_dataの中身 tuple[bytes, OperationStatus]
        rcv_data = self.serial_receive()
        # 受信データのbytes部分を渡す
        if rcv_data[0]:
            # 受信データの判別 渡すデータの例 b'\x01\x8e', b'\x02\x01\x8e'
            # bytesの型の位置にbytesを入れる
            result[0] = self.compare_and_process_receive(rcv_data[0])
        return result

    # シリアル通信を終了する際使用する関数
    def serial_close(self) -> OperationStatus:
        try:
            self.is_shutdown = ShutdownStatus.SHUTDOWN
            # シリアル通信の経路を閉じる 戻り値(OperationStatus)
            return super().serial_close()  # 親クラスのメソッドを呼び出し
        except Exception as e:
            log_error(self, self.serial_close.__name__, e)
            return OperationStatus.FAILURE
