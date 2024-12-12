# SERIAL/manager/do_serial.py

# 自作プログラムをimport
# 型チェックのデコレータ, エラー文表示
from UTILS.type_check import type_check_decorator
import UTILS.log_config as log
# 定数ファイル
from SERIAL.constant.Status    import OperationStatus
# 自作辞をを管理するクラス
from SERIAL.manager.dict_manager import DictManager
# PLCとの通信処理に基づいた処理を行うクラス
from SERIAL.manager.plc_communicator import PLCCommunicator

# ログを作成
logger = log.setup_logging()

class PLCBaseHandler:
    def __init__(self, plc_communicator: PLCCommunicator):
        # 辞書の管理
        self.do_dict: DictManager = DictManager()
        # シリアル通信
        self.plc_communicator: PLCCommunicator = plc_communicator        

    # 受信処理（ループなし）
    def receive(self):
        try:
            # シリアル通信でデータを受信
            data, status = self.plc_communicator.read()
            if status == OperationStatus.SUCCESS:
                # 受信データを処理
                self.process_received_data(data)
        except Exception as e:
            logger.error(f"{self}: {self.receive.__name__}: {e}")

    # 送信処理
    @type_check_decorator({'data': bytes})
    def send(self, data: bytes):
        try:
            # シリアル送信処理を呼び出し
            self.plc_communicator.send(data)
            print(f"Sent data: {data}")
        except Exception as e:
           logger.error(f"{self}: {self.send.__name__}: {e}")

    # 受信データをDoDictを使用して辞書の返り値を取得
    # 辞書の返り値をUIに渡すやつとインジケータに渡すやつに渡す
    @type_check_decorator({'data': bytes})
    def process_received_data(self, data: bytes):
        try:
            # DoDictを使ってデータを処理
            msg, status = self.do_dict.get_message(data)
            if status == OperationStatus.SUCCESS:
                self.send_to_ui(msg)  # UIに結果を送信
                self.send_to_indicator(msg)  # インジケータに結果を送信
            else:
                self.send_to_indicator(["動作不良", ""])
                self.send_to_indicator(["動作不良", ""])
        except Exception as e:
            logger.error(f"{self}: {self.process_received_data.__name__}: {e}")            

    # 辞書の返り値をUIに渡す
    @type_check_decorator({'data': list})
    def send_to_ui(self, data: list[str]) -> list[str]:
        try:            
            print(f"UIに渡すデータ{data}")
            return data
        except Exception as e:
            logger.error(f"{self}: {self.send_to_ui.__name__}: {e}")            
            return ["動作不良",""]

    # 辞書の返り値をインジケータに渡す
    @type_check_decorator({'data': list})
    def send_to_indicator(self, data: list[str]) -> list[str]:
        try:
            print(f"インジケータに渡すデータ{data}")
            return data
        except Exception as e:
            logger.error(f"{self}: {self.send_to_indicator.__name__}: {e}")
            return ["動作不良",""]

    # シリアル通信の終了
    def close(self):        
        self.plc_communicator.serial_close()

if __name__ == '__main__':
    pass

