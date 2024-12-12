import unittest
from unittest.mock import MagicMock
from do_serial      import DoSerial

class TestDoSerial(unittest.TestCase):
    def setUp(self):
        # DoDict と SerialManager をモック化
        self.mock_do_dict = MagicMock()
        self.mock_serial_manager = MagicMock()
        
        # DoSerial インスタンスを作成
        self.do_serial = DoSerial(self.mock_do_dict, self.mock_serial_manager)
        
        # モック化された send_to_ui メソッドをテスト用に置き換え
        self.do_serial.send_to_ui = MagicMock()

    def test_receive_data(self):
        # テストデータ（仮に正常データ）
        data = (b'\x01\x8f', True)
        
        # モックの振る舞いを設定
        self.mock_do_dict.get_message.return_value = "Processed message"
        
        # メソッドを実行
        self.do_serial.process_received_data(data)
        
        # send_to_ui が "Processed message" と呼ばれたかを確認
        self.do_serial.send_to_ui.assert_called_with("Processed message")

if __name__ == '__main__':
    unittest.main()
