from typing import Optional

class SerialDataFormatter:
    @staticmethod
    def format_send(byte: bytes) -> Optional[bytes]:
        """
        送信データをフォーマットする。

        引数:
            byte (bytes): 送信するバイトデータ

        戻り値:
            Optional[bytes]: フォーマットされたデータ（プレフィックスとサフィックスを追加）
                             None の場合はフォーマットできなかったことを示す
        """
        if byte is not None:
            return b'\x00\x01' + byte + b'\r\n'  # プレフィックスとサ
