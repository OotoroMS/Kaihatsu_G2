# test1.py

from do_serial     import DoSerial
from unittest.mock import MagicMock
from serial_manager_mock import MockSerialManager

# モッククラスを作成する
class MockPCManager:
    def get_msg(self, data: bytes):
        # データをそのまま文字列として返す仮実装
        return {"message": f"Processed data: {data}"}

# DoSerialクラスをテストする
def test_do_serial():
    # モックインスタンスを作成
    pc_manager = MockPCManager()
    serial_manager = MockSerialManager()

    # DoSerialインスタンスを作成
    do_serial = DoSerial(pc_manager, serial_manager)

    # 受信処理をテスト（本来はスレッド化して動作する部分）
    data = serial_manager.receive()  # データを受信
    do_serial.process_received_data(data)  # 受信データを処理

    # UIとインジケータに送信するメッセージがコンソールに表示されるか確認
    print("Test result for UI:")
    do_serial.send_to_ui({"message": f"Processed data: {data}"})

    print("Test result for Indicator:")
    do_serial.send_to_indicator({"message": f"Processed data: {data}"})

    # 送信処理のテスト
    test_data = b'\x01\x8f'  # テスト送信データ
    do_serial.set_and_send(test_data)  # データを送信

# テスト実行
test_do_serial()
