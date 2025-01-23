# SERIAL/manager/do_dict.py

from typing import Optional, Dict, Tuple

# 自作プログラムをimport
# 型チェックのデコレータ, エラー文表示
from UTILS.type_check import type_check_decorator
import UTILS.log_config as log
# 作成した辞書
# この２つは key = bytes value = list[str]
from SERIAL.dict.error      import comand as error
from SERIAL.dict.normal     import comand as normal
# これは    key = tuple[str] value = bytes
from SERIAL.dict.plc_cmd    import comand as comand
# 定数ファイル
from SERIAL.constant.Status import OperationStatus

# 辞書定義
ERROR_OR_NORMAL = {
    b'\x01': normal,
    b'\x02': error
}

CMD_DICT = comand

# ログを作成
logger = log.setup_logging()

class DictManager:
    # どちらの辞書を使用するか選択
    # @type_check_decorator({'data': bytes})
    def compare_dict(self, data: bytes) -> tuple[dict, OperationStatus]:
        try:
            if len(data) < 1:
                raise ValueError("辞書の情報が含まれていません。")
            # 正常か異常の判別部分を切り取り
            category = data[0:1]
            # 正常の辞書か異常の辞書どちらを使用するか選択
            command_dict = ERROR_OR_NORMAL.get(category, {})
            if not command_dict:
                raise ValueError(f"辞書が存在しません: {category}")
            return command_dict, OperationStatus.SUCCESS
        except Exception as e:
            logger.error(f"{self}: {self.compare_dict.__name__}: {e}")
            return {}, OperationStatus.FAILURE


    # 辞書からデータを探して戻り値で渡す bytes → list[str]
    # @type_check_decorator({'command_dict': dict})
    def bytes_to_list(self, command_dict: dict[bytes, list[str]], 
                      data: bytes) -> tuple[list[str], OperationStatus]:
        try:
            if len(data) < 2:
                raise ValueError("コマンドデータが含まれていません。")
            # 辞書から値を取得
            text = command_dict.get(data[1:], None)
            return text, OperationStatus.SUCCESS
        except Exception as e:
            logger.error(f"{self}: {self.bytes_to_list.__name__}: {e}")
            return ["動作不良", ""], OperationStatus.FAILURE

        
    # 辞書からデータを探して戻り値で渡す str → bytes
    # @type_check_decorator({'msg': str})
    def str_to_byte(self, msg: str) -> Optional[bytes]:
        try:            
            cmd = CMD_DICT.get(msg, b'')
            return cmd, OperationStatus.SUCCESS
        except Exception as e:
            logger.error(f"{self}: {self.str_to_byte.__name__}: {e}")
            return None, OperationStatus.FAILURE

    # 受け取ったデータから対応する文字列を返す
    # @type_check_decorator({'data': bytes})
    def get_message(self, data: bytes) -> tuple[list[str], OperationStatus]:
        try:
            command_dict, status = self.compare_dict(data)
            if status == OperationStatus.SUCCESS:
                # 戻り値 例 ["正常001", "投入部"], OperationStatus.SUCCESS
                return self.bytes_to_list(command_dict, data), status
            else:
                return ["動作不良", ""], OperationStatus.FAILURE
        except (ValueError, TypeError) as e:
            logger.error(f"{self}: {self.get_message.__name__}: {e}")
            return ["動作不良", ""], OperationStatus.FAILURE
"""
    # 動作テスト用関数
    @type_check_decorator({'data': bytes})
    def test(self, data: bytes) -> tuple[list[str], OperationStatus]:
        try:            
            command_dict = self.compare_dict(data)
            text = self.bytes_to_list(command_dict, data) if command_dict else "無効なカテゴリ"
            return text, OperationStatus.SUCCESS
        except (ValueError, TypeError) as e:            
            log_error(self, self.test.__name__, e)
            return ["動作不良", ""], OperationStatus.FAILURE
"""    

# テスト用コード（DoDictクラスのテスト）
if __name__ == '__main__':
    pass
