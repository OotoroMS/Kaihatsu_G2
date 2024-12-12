from typing import Optional
from time import perf_counter
import serial

from do_dict import DoDict
from plc_pc import SerialManager
from serial_manager_mock import MockSerialManager  # モッククラスをインポート
from type_check import type_check_decorator
import log_error

ERROR_OR_NORMAL = {
    b'\x01': "normal",
    b'\x02': "error"
}

ELAPSED_TIME = 0.0

# PCManagerクラスの定義（DoDictを使う）
class PCManager(SerialManager):
    def __init__(self, serial_params: dict):                
        # 親クラスのコンストラクタを呼び出す
        super().__init__(serial_params)
        # 辞書を管理するクラス
        self.do_dict: DoDict = DoDict()
    
    # 書き込み用
    @type_check_decorator({'data': bytes})
    def write_serial(self, data: bytes) -> Optional[bool]:
        try:
            return super().send(data)
        except Exception as e:
            log_error(self, self.write_serial.__name__, e)
    
    # 読み取り用
    def read_serial(self) -> tuple[bytes, bool]:
        try:
            result = super().receive()
            return result
        except Exception as e:
            log_error(self, self.read_serial.__name__, e)
            return b'', False
    
    # 受け取ったデータに基づいてメッセージを返す
    def read(self) -> list[str]:
        text = ["", ""]
        try:
            # dataの中身 [bytes, bool]
            data = self.read_serial()
            # data[0] = bytes
            if data[0]:
                text = self.do_dict.get_message(data[0])
                return text
            else:
                return ["動作不良", ""]
        except Exception as e:            
            log_error(self, self.read.__name__, e)
            return ["動作不良", ""]
    
    # 動作テスト用関数(全体)
    def test(self, data: bytes) -> list[str]:
        try:
            text = self.do_dict.test(data)  # DoDictのtestメソッドを使用
            return text
        except Exception as e:
            log_error(self, self.test.__name__, e)
            return ["動作不良", ""]

# テスト用コード（PCManagerクラスのテスト）
if __name__ == '__main__':
    try:
        # SerialManagerのモックインスタンスを作成（テスト用データをセット）
        mock_data = b'\x01\x8e'  # 受信するモックデータ
        serial_manager = MockSerialManager(data_to_send=mock_data)

        # PCManagerインスタンスを作成
        pc_manager = PCManager(serial_manager)

        # コマンドメッセージ取得
        result = pc_manager.read()  # read() を呼び出してメッセージを取得
        print(f"PCManager Test - read: {result}")  # 出力されるメッセージを確認

        # 動作テスト
        test_result = pc_manager.test(mock_data)
        print(f"PCManager Test - test: {test_result}")

    except Exception as e:
        print(f"PCManager Test: main: {e}")
