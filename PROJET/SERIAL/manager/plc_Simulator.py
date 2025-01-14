# SERIAL/manager/plc_pc.py

from typing import Optional, Tuple
import struct

# 自作プログラムをimport
# 型チェックのデコレータ, エラー文表示
from PROJET.UTILS.type_check import type_check_decorator
import PROJET.UTILS.log_config as log
# 定数ファイル 
from PROJET.SERIAL.constant.Status     import ResponseStatus, OperationStatus
from PROJET.SERIAL.constant.Format     import PLCDataPrefix, LineEnding
# シリアル通信のクラス(このクラスの親)
from PROJET.SERIAL.manager.serial_communicator import SerialCommunicator

# PLCとの通信処理に基づいた処理を行うクラス
class PLCSimulator(SerialCommunicator):
    def __init__(self, serial_params: dict):
        # 親クラスのコンストラクタを呼び出す
        super().__init__(**serial_params)

        self.is_response: ResponseStatus = ResponseStatus.NOT_WAITING
        self.send_data: bytes = b''

    def format_int(self, data: int) ->bytes:
        bytes_data = struct.pack(">B", data)
        return bytes_data

    # 引数の値を成形して返す
    """ (例)
        引数:PLCDataPrefix.DATA_IN, PLCDataPrefix.ERROR, b'\x2c'   戻り値:b'\x01\x02\x2c\n'
        引数:PLCDataPrefix.ACK, PLCDataPrefix.NORMAL, b'\x2c'       戻り値:b'\x02\x01\x2c\n'
    """
    def format_bytes(self, prefix1: PLCDataPrefix, prefix2: PLCDataPrefix, data: bytes) -> bytes:
        format_data = prefix1.value + prefix2.value + data + LineEnding.LF.value
        self.logger.debug(f"成形前データ:{data}\n成形後データ{format_data}")
        return format_data
    
    # 送信の流れ
    """ (例)
        引数: b'\x2c' 
        成形データ: b'\x01\x02\x2c\n' 
        返値:OperationStatus.SUCCESS            
    """
    def send(self, data: bytes) -> OperationStatus:
        send_data = self.format_bytes(PLCDataPrefix.DATA_IN, PLCDataPrefix.ERROR, data)  # データの成形
        if self.is_response == ResponseStatus.NOT_WAITING:
            result = super().serial_write(send_data)  # 送信            
            if result == OperationStatus.FAILURE:
                return result
            self.send_data = data
            self.is_response = ResponseStatus.WAITING
            return result
        return OperationStatus.FAILURE
    
    # 受信の流れ
    """ (例)
        引数: なし
        返値: (b'\x01\x2c', OperationStatus.SUCCESS)
              (b'', OperationStatus.FAILURE)
    """
    def read(self) -> tuple[bytes, OperationStatus]:
        data, status = super().serial_read()  # シリアルポートからデータを受信
        if status == OperationStatus.FAILURE:
            return data, status
        rcv_data, status = self.compare_and_process(data)  # 受信データを判別して処理
        return rcv_data, status

    # 受信データの長さ確認
    """ (例)
        引数: b'\x01\x2c' 
        返値: OperationStatus.SUCCESS
    """
    def valid_data(self, data: bytes) -> OperationStatus:
        if len(data) < 1:  # 受信データの長さが2未満の場合
            self.logger.error(f"受信データの長さが足りません")
            return OperationStatus.FAILURE
        return OperationStatus.SUCCESS

    # 受信データの判別と処理
    """ (例)
        引数: b'\x01\x2c' 
        返値: (b'\x2c', OperationStatus.SUCCESS)    
    """
    def compare_and_process(self, data: bytes) -> tuple[bytes, OperationStatus]:
        if self.valid_data(data) == OperationStatus.FAILURE:
            return b'', OperationStatus.FAILURE

        if data.startswith(PLCDataPrefix.DATA_IN.value):  # DATA_INが接頭語の場合
            self.logger.debug(f"PLCからの送信データ")
            cmd = data[1:2]  # コマンドデータ
            status = self.response(cmd)  # 応答送信
            if status == OperationStatus.FAILURE:
                return b'', status
            return cmd, status
        elif data.startswith(PLCDataPrefix.ACK.value):  # ACKが接頭語の場合
            self.logger.debug(f"PLCからの応答データ")
            self.is_response = ResponseStatus.NOT_WAITING  # 応答待ち解除
            cmd = data[1:2]  # コマンドデータ
            status = self.compare(cmd)  # データ比較
            if status == OperationStatus.FAILURE:
                self.send(cmd)  # 再送                
            return b'', OperationStatus.FAILURE
        
        self.is_response = ResponseStatus.NOT_WAITING  # 応答待ち解除
        return b'', OperationStatus.FAILURE

    # 応答を返す
    """ (例)
        引数: b'\x2c'
        成形データ: b'\x02\x01\x2c'
        返値: OperationStatus.SUCCESS または OperationStatus.FAILURE
    """
    def response(self, data: bytes) -> OperationStatus:
        response_data = self.format_bytes(PLCDataPrefix.ACK, PLCDataPrefix.NORMAL, data)  # 応答データ成形
        result = super().serial_write(response_data)  # 応答送信
        self.logger.debug(f"応答を送信します。")
        return result

    # 送信データの比較
    """ (例)
        引数: b'\x2c'
        返値: OperationStatus.SUCCESS        
    """
    def compare(self, data: bytes) -> OperationStatus:
        if data == self.send_data:
            self.logger.debug(f"受信データの中身:OK")
            return OperationStatus.SUCCESS
        self.logger.debug(f"受信データの中身:NG")
        return OperationStatus.FAILURE

if __name__ == '__main__':
    pass