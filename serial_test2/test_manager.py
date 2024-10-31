import time
from queue_create import QueueCreate
from serial_manager import SerialManager
import serial

# シリアルポートの設定
PORT1 = "COM5"  # 適切なポートに変更してください
PORT2 = "COM3"  # 適切なポートに変更してください
BAUD_RATE = 9600
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE
TIMEOUT = 0.1


# シリアルパラメータとキューの初期設定
serial_params1 = {
    "port": PORT1,
    "baudrate": BAUD_RATE,
    "party": PARITY,
    "stopbits": STOPBITS,
    "timeout": TIMEOUT,
}

serial_params2 = {
    "port": PORT1,
    "baudrate": BAUD_RATE,
    "party": PARITY,
    "stopbits": STOPBITS,
    "timeout": TIMEOUT,
}

class TestManager:
    def __init__(self, queues: dict):        
        serial_conn1 = SerialManager(serial_params1, queues)
        serial_conn2 = SerialManager(serial_params2, queues)

    def test_process_send_data():
        pass

    def measure_time(func, *args, **kwargs):
        """
        関数の実行時間を測定するラッパー関数。

        引数:
            func (callable): 測定対象の関数
            *args: 関数に渡す引数
            **kwargs: 関数に渡すキーワード引数

        戻り値:
            実行時間 (float): 秒単位の実行時間
        """
        start_time = time.time()  # 開始時間を記録
        func(*args, **kwargs)  # 関数を実行
        end_time = time.time()  # 終了時間を記録
        return end_time - start_time  # 実行時間を返す


def main():
    queue = QueueCreate()
    queues = queue.get_communication_queues()
    TestManager(queues)

if __name__ == '__main__':
    main()