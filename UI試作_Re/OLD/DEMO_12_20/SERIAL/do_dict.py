from typing import Optional, Dict, Tuple

from SERIAL.error      import comand as error
from SERIAL.normal     import comand as normal
from SERIAL.plc_cmd    import comand as comand
from SERIAL.type_check import type_check_decorator
import SERIAL.log_error as log_error

# 辞書定義
ERROR_OR_NORMAL = {
    b'\x01': normal,
    b'\x02': error
}

CMD_DICT = comand

class DoDict:
    # どちらの辞書を使用するか選択
    @type_check_decorator({'data': bytes})
    def compare_dict(self, data: bytes) -> Optional[dict]:        
        try:
            if len(data) < 1:
                raise ValueError("辞書の情報が含まれていません。")
            # 正常か異常の判別部分を切り取り
            category = data[0:1]
            # 正常の辞書か異常の辞書どちらを使用するか選択
            command_dict = ERROR_OR_NORMAL.get(category)
            # ここで辞書が存在すれば辞書を返す            
            if command_dict is None:
                raise ValueError(f"辞書が存在しません: {category}")
            return command_dict
        except Exception as e:
            log_error(self, self.compare_dict.__name__, e)
            return None

    # 辞書からデータを探して戻り値で渡す bytes → list[str]
    @type_check_decorator({'command_dict': dict, 'data': bytes})
    def get_cmd_msg(self, command_dict: dict[bytes, list[str]], data: bytes) -> Optional[list[str]]:
        text = []
        try:
            if len(data) < 2:
                raise ValueError("コマンドデータが含まれていません。")
            # 辞書から値を取得
            text = command_dict.get(data[1:], ["不明なコマンド"])
            return text
        except Exception as e:
            log_error(self, self.get_cmd_msg.__name__, e)
            return None
        
    # 辞書からデータを探して戻り値で渡す list[str] → bytes
    @type_check_decorator({'msg': tuple})
    def get_msg_cmd(self, msg: tuple[str]) -> Optional[bytes]:
        try:            
            cmd = CMD_DICT.get(msg, b'')
            return cmd
        except Exception as e:
            log_error(self, self.get_msg_cmd.__name__, e)
            return None

    # 受け取ったデータから対応する文字列を返す
    @type_check_decorator({'data': bytes})
    def get_message(self, data: bytes) -> list[str]:        
        try:
            command_dict = self.compare_dict(data)
            if command_dict:
                text = self.get_cmd_msg(command_dict, data)
                return text
            else:
                return ["動作不良", ""]
        except (ValueError, TypeError) as e:
            log_error(self, self.get_message.__name__, e)
            return ["動作不良", ""]
    
    # 動作テスト用関数
    @type_check_decorator({'data': bytes})
    def test(self, data: bytes) -> Optional[list[str]]:
        try:            
            command_dict = self.compare_dict(data)
            text = self.get_cmd_msg(command_dict, data) if command_dict else "無効なカテゴリ"
            return text
        except (ValueError, TypeError) as e:            
            log_error(self, self.test.__name__, e)
            return None

# テスト用コード（DoDictクラスのテスト）
if __name__ == '__main__':
    # DoDictクラスのインスタンス作成
    do_dict = DoDict()

    # テストデータ
    data = b'\x01\x8f'  # サンプルデータ
    cmd  = ("偏芯モータ回転"   , "投入・洗浄部")

    # コマンドメッセージ取得
    result = do_dict.get_message(data)
    print(f"DoDict Test - get_message: {result}")  # 出力されるメッセージを確認
    result = do_dict.get_msg_cmd(cmd)
    print(f"DoDict Test - get_msg_cmd: {result}")

    # 動作テスト
    test_result = do_dict.test(data)
    print(f"DoDict Test - test: {test_result}")  # 動作テスト結果
