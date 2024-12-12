# serial_manager_mock.py

class MockSerialManager:
    def __init__(self, data_to_send: bytes = b'\x01\x8e'):
        self.data_to_send = data_to_send  # モックで送信するデータ
        self.received_data = None

    # データ送信メソッドのモック
    def send(self, data: bytes):
        self.received_data = data  # 送信されたデータを保存
    
    # データ受信メソッドのモック
    def receive(self):
        return self.data_to_send, True  # モックデータを返す

