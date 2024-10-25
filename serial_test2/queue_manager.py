import struct
from queue import Queue
from typing import Optional, Union

class QueueManager:
    def __init__(self, queues: dict):
        """
        初期化メソッド。指定された辞書から送信用キューと受信用キューを設定。
        
        引数:
            queues (dict): send_queue と receive_queue を含む辞書
        """
        self.send_queue: Queue = queues['send_queue']
        self.receive_queue: Queue = queues['receive_queue']

    def get_from_queue(self, queue: Queue) -> Optional[Union[str, int, bytes]]:
        """
        指定したキューからデータを取り出して返す。キューが空の場合は None を返す。

        引数:
            queue (Queue): データを取り出す対象のキュー

        戻り値:
            Optional[Union[str, int, bytes]]: キューから取り出したデータ。キューが空の場合は None
        """
        if not queue.empty():
            return queue.get()
        return None

    def put_in_queue(self, queue: Queue, word: Optional[Union[str, int, bytes]]) -> None:
        """
        指定したキューにデータを追加する。データが None の場合は何もしない。

        引数:
            queue (Queue): データを追加する対象のキュー
            word (Optional[Union[str, int, bytes]]): 追加するデータ
        """
        if word is not None:
            queue.put(word)

    def send_queue_item(self) -> Optional[bytes]:
        """
        send_queue からデータを取り出し、バイト型に変換して返す。キューが空の場合は None を返す。

        戻り値:
            Optional[bytes]: バイト型に変換されたデータ。キューが空の場合は None
        """
        word = self.get_from_queue(self.send_queue)
        if word is None:
            return None        
        return self.to_byte(word)

    def to_byte(self, word: Union[str, int, bytes]) -> Optional[bytes]:
        """
        データをバイト型に変換して返す。データが文字列の場合は UTF-8 でエンコードし、
        数字の場合は1バイトの整数としてエンコードする。バイト型の場合はそのまま返す。

        引数:
            word (Union[str, int, bytes]): バイト型に変換するデータ

        戻り値:
            Optional[bytes]: バイト型に変換されたデータ。無効なデータ型の場合は None
        """
        if isinstance(word, str):
            return word.encode('utf-8') if not word.isdigit() else struct.pack('>B', int(word))
        elif isinstance(word, int):
            return struct.pack('>B', word)
        elif isinstance(word, bytes):
            return word
        else:
            print("Invalid data type")
            return None
