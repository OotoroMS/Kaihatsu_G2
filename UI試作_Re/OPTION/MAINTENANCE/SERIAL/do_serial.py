from do_dict import DoDict
from plc_pc import SerialManager
import SERIAL.log_error as log_error
from SERIAL.type_check import type_check_decorator

# PLCとのやり取りを監視して、結果を各クラスに渡す
class DoSerial:
    def __init__(self, serial_manager: SerialManager):
        # 辞書の管理
        self.do_dict: DoDict = DoDict()
        # シリアル通信
        self.serial_manager: SerialManager = serial_manager  # SerialManager インスタンスを設定
        self.is_loop: bool = True

    # 受信ループ処理
    # この関数はスレッド化する予定
    def receive_loop(self):
        while self.is_loop:
            try:
                # シリアル通信でデータを受信
                data = self.serial_manager.receive()
                if data[0]:
                    # 受信データを処理
                    self.process_received_data(data[0])
            except Exception as e:
                log_error(self, self.receive_loop.__name__, e)

    # 送信処理
    # 引数に渡した値を送信させる
    @type_check_decorator({'data': bytes})
    def send(self, data: bytes):
        try:
            # シリアル送信処理を呼び出し
            self.serial_manager.send(data)
            print(f"Sent data: {data}")
        except Exception as e:
            log_error(self, self.send.__name__, e)

    
    # 送信データ獲得
    @type_check_decorator({'data': tuple})
    def set_send_data(self, data: tuple[str]) -> bytes:
        # 辞書を使用して引数に対応するbytesを    
        # 送信データとして返す
        result = self.do_dict.get_msg_cmd(data)
        return result

    # 送信データ獲得＋送信
    @type_check_decorator({'data': tuple})
    def set_and_send(self, data: tuple[str]):
        send_data = self.set_send_data(data)
        if send_data:
            # self.send(send_data)
            # デバック用
            print(send_data)


    # 受信データをDoDictを使用して辞書の返り値を取得
    # 辞書の返り値をUIに渡すやつとインジケータに渡すやつに渡す
    @type_check_decorator({'data': bytes})
    def process_received_data(self, data: bytes):
        try:
            # DoDictを使ってデータを処理
            result = self.do_dict.get_message(data)  
            self.send_to_ui(result)  # UIに結果を送信
            self.send_to_indicator(result)  # インジケータに結果を送信
        except Exception as e:
            log_error(self, self.process_received_data.__name__, e)

    # 辞書の返り値をUIに渡す
    @type_check_decorator({'data': list})
    def send_to_ui(self, data: list[str]) -> list[str]:
        try:            
            print(f"UIに渡すデータ{data}")
            return data
        except Exception as e:
            log_error(self, self.send_to_ui.__name__, e)            
            return ["動作不良",""]

    # 辞書の返り値をインジケータに渡す
    @type_check_decorator({'data': list})
    def send_to_indicator(self, data: list[str]) -> list[str]:
        try:
            print(f"インジケータに渡すデータ{data}")
            return data
        except Exception as e:
            log_error(self, self.send_to_indicator.__name__, e)
            return ["動作不良",""]
    
    def colse(self):
        self.is_loop = False
        self.serial_manager.serial_close()

if __name__ == '__main__':

    do_serial = DoSerial(None)

    cmd = ("偏芯モータ回転"   , "投入・洗浄部")
    result = do_serial.set_send_data(cmd)
    print(result)
    do_serial.set_and_send(cmd)
