# """
# 概要：
# バイトデータから測定値を取得するモジュール。
# convertion_byte_froat() を実行すれば値を取得できる。
# 関数一覧：
#     judge_error(base_array) : エラーの判定を行う関数
#     conversion_meas_bytearray(base_array) : 渡されたバイト配列から正負記号と測定値を取得する関数
#     convertion_meas_froat(base_array) : 渡されたバイト配列をfloat型に変換する関数
#     convertion_byte_froat(byte) : 渡されたバイトデータから測定値を取得する関数
# """
# from ExtracionMeas import *
# from MeasConvert import *

# def judge_error(base_array : bytearray) -> float:
#     """
#     受け取ったバイト配列からｴﾗｰ内容を識別する関数。
#     データ入力エラーなら -101,フォーマットエラーなら -102を返す。

#     Parameters:
#     base_array (bytearray)  : 識別対象のバイト配列

#     Returns:
#     float : 入力エラーなら -101.0,フォーマットエラーなら -102.0。
#     """
#     if len(base_array) > 2:
#         if base_array[2] == 49: #   ASCIIコードで'1'は49
#             return -101.0     #   データが入力されていない
#         else:
#             return -102.0     #   取り込んだフォーマットが規定フォーマットでない
#     else:
#         return -102.0

# def conversion_meas_bytearray(base_array : bytearray) -> Tuple[Optional[int], bytearray]:
#     """
#     渡されたバイト配列から測定値のみを抜き出すまでの処理をまとめた関数。
#     正負記号と抜き出した測定値のバイト配列を返す。
#     正負記号がない、または測定値のバイト配列がなければ Noneと空のバイト配列を返す。
    
#     Parameters:
#     base_array (bytearray)  : 抜き出す対象のバイト配列

#     Returns:
#     Tuple[Optional[int], bytearray] : 正負記号(正負記号がなければNone), 取得したバイト配列
#     """
#     sign, sign_index = search_sign(base_array)
#     delete_cr_array = delete_cr(base_array)
#     meas_array = extraction_meas(delete_cr_array, sign_index)
#     if meas_array and sign:
#         return sign, meas_array
#     else:
#         return None,  bytearray()

# def convertion_meas_froat(base_array : bytearray) -> Optional[float]:
#     """
#     渡されたバイト配列から測定値をfloat型で取得する関数.
#     正負記号の取得に成功し、測定値のバイト配列が小数点を含む数値のみのとき、
#     バイト配列からfloat型に変換し、正負記号を反映した値を返す。
#     取得に失敗した、または小数点を含む数値以外の時,Noneを返す。
     
#     Parameters:
#     base_array (bytearray)  : 抜き出す対象のバイト配列

#     Returns:
#     Optional[float] : 変換した値(失敗時はNone)
#     """
#     sign, meas_array = conversion_meas_bytearray(base_array)

#     if sign and confim_bytearray_number(meas_array):
#         decimal_index = search_decimal_index(meas_array)
#         place_value = calculate_radix(decimal_index)
#         if place_value > -1:
#             intger_array, decimal_array = divide_bytearray(meas_array,decimal_index)
#             intger_value = conversion_bytearray_float(intger_array,  place_value)
#             decimal_value = conversion_bytearray_float(decimal_array, 0.1)
#             convertion_result = intger_value + decimal_value
#             if sign == 45:   #   正負記号がASCIIコードで45（"-"）なら
#                 convertion_result = -convertion_result
#             return convertion_result
#     return None

# def convertion_byte_froat(byte : bytes) -> float:
#     """
#     受け取ったbyteデータから測定値を取得する関数。
#     エラーがなければconvertion_meas_froatの実行結果を返す。
#     エラーがあれば、judge_errorの実行結果を返す。
    
#     Parameters:
#     byte (bytes)  : 測定値を抜き出すバイトデータ

#     Returns:
#     float :  onvertion_meas_froatの実行結果、またはjudge_errorの実行結果
#     """
#     origen_array = bytearray(byte)

#     #   エラーデータの判定
#     if (origen_array[0], origen_array[1]) == (57, 49):    #   ASCIIコードで"9"は57,"1"は49
#         return judge_error(origen_array)
#     else:
#         return convertion_meas_froat(origen_array)
         
# if __name__ == "__main__":
#     byte = {
#         b'01A+000.0101\r',
#         b'01A+11111111\r',
#         b'01A+000.1111\r',
#         b'01A+111.0000\r',
#         b'01A+000.0000\r',
#         b'911\r',
#         b'912\r'
#     }
#     for i in byte:
#         result = convertion_byte_froat(i)
#         print("bytes :",str(i)," result:", result)

from DEGITALINDICATOR.ExtracionMeas import *
from DEGITALINDICATOR.MeasConvert   import *

def judge_error(base_array: bytearray) -> float:
    if len(base_array) > 2:
        if base_array[2] == 49:
            return -101.0
        else:
            return -102.0
    else:
        return -102.0

def conversion_meas_bytearray(base_array: bytearray) -> Tuple[Optional[int], bytearray]:
    sign, sign_index = search_sign(base_array)
    delete_cr_array = delete_cr(base_array)
    meas_array = extraction_meas(delete_cr_array, sign_index)
    if meas_array and sign:
        return sign, meas_array
    else:
        return None, bytearray()

def convertion_meas_froat(base_array: bytearray) -> Optional[float]:
    sign, meas_array = conversion_meas_bytearray(base_array)
    if sign and confim_bytearray_number(meas_array):
        decimal_index = search_decimal_index(meas_array)
        place_value = calculate_radix(decimal_index)
        if place_value > -1:
            intger_array, decimal_array = divide_bytearray(meas_array, decimal_index)
            intger_value = conversion_bytearray_float(intger_array, place_value)
            decimal_value = conversion_bytearray_float(decimal_array, 0.1)
            convertion_result = intger_value + decimal_value
            if sign == 45:
                convertion_result = -convertion_result
            return convertion_result
    return None

def convertion_byte_froat(byte: bytes) -> float:
    origen_array = bytearray(byte)
    if (origen_array[0], origen_array[1]) == (57, 49):
        return judge_error(origen_array)
    else:
        return convertion_meas_froat(origen_array)

if __name__ == "__main__":
    byte = {
        b'01A+000.0101\r',
        b'01A+11111111\r',
        b'01A+000.1111\r',
        b'01A+111.0000\r',
        b'01A+000.0000\r',
        b'911\r',
        b'912\r'
    }
    for i in byte:
        result = convertion_byte_froat(i)
        print("bytes :", str(i), " result:", result)
