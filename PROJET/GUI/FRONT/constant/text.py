# GUI/FRONT/constant/text.py

# 各テキストの設定をまとめたファイル
from enum import Enum

# 自作プログラムをimport
# 定数ファイル
from GUI.FRONT.constant.color import WHITE

class TextBase(Enum):
    # 共通のボタン設定（親クラス）
    def __init__(self, pos, text, color):
        self.pos = pos      # テキストの座標
        self.text = text    # テキストの内容
        self.color = color  # テキストの色   

class TextEnd(TextBase):
    End = ((950, 400), "終了しますか？", WHITE)

class TextOriginReset(TextBase):
    Reset = ((950, 200), "原点復帰を行います。\n装置内に異物が無いことを確認して\n「はい」を押してください。", WHITE)

class TextMeasure(TextBase):
    View = ((950, 400), "", WHITE)