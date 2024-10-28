"""
概要：
測定値をfloatに変換する処理をまとめたモジュール。
関数一覧：
    search_decimal_index(base_bytearray) : 小数点のインデックスを探す関数
    calculate_radix(decimal_index) : 小数点のインデックスから基数を求める関数
    confim_bytearray_number(base_bytearray) : 受け取ったバイト配列の中身が規定の値になっているか確認する関数
    divide_bytearray(base_bytearray, decimal_index) : 渡されたバイト配列を小数点の位置で分割する関数
    conversion_bytearray_float(base_bytearray, place_value) : 渡されたバイト配列をfloat型に変換する関数
"""
from typing import Tuple

def search_decimal_index(base_bytearray : bytearray) -> int:
    """
    受け取った配列内からASCIIコードの"."（小数点）があるか探し
    そのインデックスを返す関数。
    ASCIIコードの"."を検知した時点でのindexの値を返す。
    存在しなければ、-1を返す。

    Parameters:
    base_bytearray (bytearray)  : 検出対象のバイト配列

    Returns:
    int : 小数点のインデックス。存在しなければ -1。
    """

    ASCII_DECIMAL  = 46    #   ASCIIコード46は小数点

    for index, byte in enumerate(base_bytearray):
        if byte == ASCII_DECIMAL:
            return index

    return -1

def calculate_radix(decimal_index : int) -> int:
    """
    search_decimal_indexで求めた小数点のインデックスから整数部の基数を計算する関数。
    decimal_indexが1以上なら、10の(decimal_index - 1)乗の値を返す。
    decimal_indexが0未満なら -1 を返す。

    Parameters:
    base_bytearray (bytearray)  : 検出対象のバイト配列

    Returns:
    int : 10の(decimal_index - 1)乗。decimal_indexが0未満の場合は -1。
    """
    if (decimal_index - 1) >= 0:
        return 10 ** (decimal_index - 1)
    else:
        return -1

def confim_bytearray_number(base_bytearray : bytearray) -> bool:
    """
    受け取ったバイト配列が小数点と0から9の数字のみで構成されているか確認する関数。
    それ以外の文字が含まれている場合は False を返す。

    Parameters:
    base_bytearray (bytearray)  : 検出対象のバイト配列

    Returns:
    bool: 小数点と0から9の数字のみで構成されていれば True,
          それ以外の値があれば False。
    """
    ASCII_DECIMAL  = 46    #   ASCIIコード46は小数点
    ASCII_ZERO = 48
    ASCII_NINE = 57
    for byte in base_bytearray:
        # 小数点でも数字でもない場合は False
        if byte != ASCII_DECIMAL and not (ASCII_ZERO <= byte <= ASCII_NINE):
            return False
    
    return True

def divide_bytearray(base_bytearray : bytearray, decimal_index : int) -> Tuple[bytearray, bytearray]:
    """
    受け取ったバイト配列を整数部と小数部に分ける関数。
    decimal_indexより前なら整数部のバイト配列に追加し、
    decimal_indexより後なら小数部のバイト配列に追加する。
    小数点そのものは無視される。

    Parameters:
    base_bytearray (bytearray)  : 検出対象のバイト配列
    decimal_index (int): 小数点のインデックス

    Returns:
    Tuple[bytearray, bytearray] : 整数部と小数部のバイト配列
    """
    # 整数部: 小数点より前の部分
    integer_bytearray = base_bytearray[:decimal_index]
    
    # 小数部: 小数点より後の部分
    decimal_bytearray = base_bytearray[decimal_index + 1:]
    
    return integer_bytearray, decimal_bytearray

def conversion_bytearray_float(base_bytearray : bytearray, place_value) -> float:
    """
    受け取ったバイト配列を浮動小数点型に変換する関数。

    Parameters:
    base_bytearray (bytearray)  : 変換対象のバイト配列
    place_value : 基数（10の乗数で表される）
    
    Returns:
    float : バイト配列を変換した値
    """
    ASCII_ZERO = 48
    converted_value = 0.0

    for byte in base_bytearray:
        converted_value += ((byte - ASCII_ZERO) * place_value)
        place_value /= 10
    
    return converted_value
