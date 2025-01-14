import serial
import logging
from typing import Tuple
from SERIAL.constant.Status import OperationStatus
from SERIAL.constant.Format import DataPrefix, LineEnding
from UTILS.log_config import setup_logging
from SERIAL.manager.serial_communicator import SerialCommunicator

class PLCProtocolCommunicator(SerialCommunicator):
    def __init__(self, port: str, baudrate: int = 9600, parity: str = serial.PARITY_NONE, stopbits: int = serial.STOPBITS_ONE, timeout: float = 1.0):
        """
        PLCとの通信をフォーマットに基づいて行うクラスを初期化します。

        Args:
            port (str): シリアルポート名 (例: "COM3")。
            baudrate (int): ボーレート。デフォルトは9600。
            parity (str): パリティビット設定。デフォルトはPARITY_NONE。
            stopbits (int): ストップビット設定。デフォルトはSTOPBITS_ONE。
            timeout (float): タイムアウト秒数。デフォルトは1.0秒。
        """
        super().__init__(port, baudrate, parity, stopbits, timeout)
        self.logger = setup_logging()

    def format_bytes(self, prefix1: DataPrefix, prefix2: DataPrefix, data: bytes) -> bytes:
        """
        フォーマットに基づいて送信データを構築します。

        Args:
            prefix1 (DataPrefix): 最初の接頭語。
            prefix2 (DataPrefix): 2番目の接頭語。
            data (bytes): 実際のデータ。

        Returns:
            bytes: フォーマット済みデータ。
        """
        formatted_data = prefix1.value + prefix2.value + data + LineEnding.LF.value
        self.logger.debug(f"成形データ: {formatted_data}")
        return formatted_data

    def send_data(self, prefix1: DataPrefix, prefix2: DataPrefix, data: bytes) -> OperationStatus:
        """
        フォーマット済みデータをPLCに送信します。

        Args:
            prefix1 (DataPrefix): 最初の接頭語。
            prefix2 (DataPrefix): 2番目の接頭語。
            data (bytes): 実際のデータ。

        Returns:
            OperationStatus: SUCCESSまたはFAILURE。
        """
        try:
            formatted_data = self.format_bytes(prefix1, prefix2, data)
            return self.serial_write(formatted_data)
        except Exception as e:
            self.logger.error(f"送信エラー: {e}")
            return OperationStatus.FAILURE

    def receive_data(self) -> Tuple[bytes, OperationStatus]:
        """
        PLCからデータを受信します。

        Returns:
            Tuple[bytes, OperationStatus]: 受信データとステータス。
        """
        try:
            raw_data, status = self.serial_read()
            if status == OperationStatus.SUCCESS:
                self.logger.debug(f"受信データ: {raw_data}")
                return raw_data, OperationStatus.SUCCESS
            return b"", OperationStatus.FAILURE
        except Exception as e:
            self.logger.error(f"受信エラー: {e}")
            return b"", OperationStatus.FAILURE

    def parse_data(self, data: bytes) -> Tuple[bytes, DataPrefix]:
        """
        受信データを解析し、接頭語とデータ本体を分割します。

        Args:
            data (bytes): 受信データ。

        Returns:
            Tuple[bytes, DataPrefix]: データ本体と最初の接頭語。
        """
        try:
            if len(data) < 2:
                raise ValueError("データの長さが短すぎます。")

            prefix1 = DataPrefix(data[:1])
            body = data[1:-1]  # 最初の接頭語と終端文字を除去
            self.logger.debug(f"解析結果: 接頭語1={prefix1}, データ本体={body}")
            return body, prefix1
        except Exception as e:
            self.logger.error(f"解析エラー: {e}")
            return b"", DataPrefix.NONE

if __name__ == "__main__":
    serial_params = {
        "port": "COM3",
        "baudrate": 9600,
        "parity": serial.PARITY_NONE,
        "stopbits": serial.STOPBITS_ONE,
        "timeout": 1.0,
    }

    communicator = PLCProtocolCommunicator(**serial_params)

    if communicator.serial_open() == OperationStatus.SUCCESS:
        try:
            while True:
                raw_data, status = communicator.receive_data()
                if status == OperationStatus.SUCCESS:
                    body, prefix1 = communicator.parse_data(raw_data)
                    communicator.logger.info(f"受信データ解析: 接頭語1={prefix1}, 本文={body}")
                    communicator.send_data(DataPrefix.ACK, DataPrefix.DATA_IN, body)
                else:
                    break
        finally:
            communicator.serial_close()
