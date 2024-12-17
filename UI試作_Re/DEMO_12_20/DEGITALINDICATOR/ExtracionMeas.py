# """
# 概要：
# バイト配列から測定値を抽出する処理をまとめたモジュール。
# 関数一覧：
#     search_sign(base_bytearray) : 正負記号を探す関数
#     delete_cr(base_bytearray) : キャリッジリターンを削除する関数
#     extraction_meas(base_bytearray, sign_index) : バイト配列から測定値を抽出する関数
# """
# from typing import Tuple, Optional

# def search_sign(base_bytearray : bytearray) -> Tuple[Optional[int], int]:
#     """
#     受け取った配列内にASCIIコードの"+"または"-"があるか探す関数。
#     存在すれば記号のASCIIコードと検出インデックスを返し、
#     存在しない場合は None と -1 を返す。
    
#     Parameters:
#     base_bytearray (bytearray): 検出対象のバイト配列

#     Returns:
#     Tuple[Optional[int], int]: 記号のASCIIコード(存在しない場合はNone),及び検出インデックス
#     """
#     ASCII_PLUS = 43
#     ASCII_MINUS = 45
    
#     for index, byte in enumerate(base_bytearray):
#         if byte == ASCII_PLUS or byte == ASCII_MINUS:
#             return byte, index

#     return None, -1

# def delete_cr(base_bytearray : bytearray) -> bytearray:
#     """
#     受け取った配列内からASCIIコードのキャリッジリターン(CR)を取り除く関数。
#     CR(ASCIIコード13)を検出した時点で処理を中断し、検出までに追加したデータを返す。
#     CRが存在しない場合は元の配列全体を返す。

#     Parameters:
#     base_bytearray (bytearray): 検出対象のバイト配列

#     Returns(戻り値):
#     bytearray : CRを削除したbytearray配列
#     """

#     ASCII_CR = 13
#     cr_delete_array = bytearray()
#     for byte in base_bytearray:
#         if byte == ASCII_CR:
#             #   CRを検出した時点で追加済みデータを返す
#             return cr_delete_array
#         else:
#             cr_delete_array.append(byte)

#     #   CRが存在しなければ元の配列全体を返す
#     return cr_delete_array

# def extraction_meas(base_bytearray : bytearray, sign_index : int) -> bytearray:
#     """
#     serath_signで検出した正負記号のindexをもとに測定値を抽出する関数。
#     sign_index+1の場所から最後までのデータを抽出して返す。

#     Parameters:
#     base_bytearray (bytearray)  : 検出対象のバイト配列
#     sign_index : 小数点のインデックス
    
#     Returns:
#     bytearray : 抽出された測定値のバイト配列,sign_index+1が範囲外なら空の配列を返す。
#     """
#     #   sign_index+1が配列の長さ以内か確認し、スライスで取得
#     if sign_index + 1 < len(base_bytearray):
#         return base_bytearray[sign_index + 1:]
    
#     #   sign_index+1が範囲外の場合は空の配列を返す
#     return bytearray()

from typing import Tuple, Optional

def search_sign(base_bytearray: bytearray) -> Tuple[Optional[int], int]:
    ASCII_PLUS = 43
    ASCII_MINUS = 45
    
    for index, byte in enumerate(base_bytearray):
        if byte == ASCII_PLUS or byte == ASCII_MINUS:
            return byte, index

    return None, -1

def delete_cr(base_bytearray: bytearray) -> bytearray:
    ASCII_CR = 13
    cr_delete_array = bytearray()
    for byte in base_bytearray:
        if byte == ASCII_CR:
            return cr_delete_array
        else:
            cr_delete_array.append(byte)
    return cr_delete_array

def extraction_meas(base_bytearray: bytearray, sign_index: int) -> bytearray:
    if sign_index + 1 < len(base_bytearray):
        return base_bytearray[sign_index + 1:]
    return bytearray()
