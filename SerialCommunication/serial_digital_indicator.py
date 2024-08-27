#   デジタルインジケータからデータを取得し、float型に変換するプログラム
import serial
import time
from typing import Tuple

#   グローバル変数
#   アスキーコード
ASCII_PLAS  = 43
ASCII_MINUS = 45
ASCII_CR    = 13
ASCII_ZERO  = 48
ASCII_DECI  = 46
#   判定基準
PLAS_JUDGMENT  = 0.1
MINUS_JUDGMENT = -0.1
#   判定結果
OK         = True
NG         = False
#   送信データ
DATA_SND_MSG = 's'  #   取得命令

#   シリアルポート
COM = "COM3"

#   シリアル通信プログラム(引数:通信先、送信データ 戻り値:測定値)
def get_data(ser : serial, snd_msg : str) -> bytes:
    print("serial test start!!")
    try:
        ser.write(snd_msg.encode())     #   データ取得命令を送信
        rcv_msg = ser.read(13)          #   データを取得
    except Exception as e:              #   エラー発生時
        print("エラー\n")               #   画面にｴﾗｰの内容を表示   
        print(e)
    
    return rcv_msg

#   bytes型->bytearray型変換関数
def chenge_byte_bytearray(data : bytes) -> bytearray:
    try:
        chenge_byte = bytearray(data)   #   byte型をbytearray型に変換
        return chenge_byte              #   結果を戻す
    except Exception as e:
        print("chenge_byte_bytearray error:", e)
        return bytearray()

#   正負記号取得関数
def get_sign(ary_data : bytearray, ary_size : int) -> Tuple[int , bytes]:
    try:
        #   正負記号の位置と記号を取得
        for i in range(ary_size):
            if ary_data[i] == ASCII_PLAS or ary_data[i] == ASCII_MINUS:     #   配列のi番目に格納されているデータが"+"or"-"ならば
                sign = ary_data[i]                                          #   配列のi番目を取得
                sign_index = i                                              #   正負記号の位置を取得
        #   結果を戻す
        return sign_index, sign
    except Exception as e:
        print("get_sign error:", e)

#   測定値抽出関数
def get_meas(ary_data : bytearray, ary_size : int, sign_index : int) -> bytearray:
    try:
        meas_val = bytearray()
        for i in range(ary_size):
            if i > sign_index and ary_data[i] != ASCII_CR:      #   正負記号より後で、CRでなければ
                meas_val.append(ary_data[i])                    #   配列のi番目を配列に追加
    
        return meas_val
    except Exception as e:
        print("get_meas error:", e)

#   小数点位置取得関数
def get_decimal_index(ary_data:bytearray, ary_size:int) -> int:
    decimal_point   = 0    #   小数点位置格納変数
    try:
        #   小数点の位置を取得
        for i in range(ary_size):
            #   配列のi番目のデータが"."ならば
            if  ary_data[i] == ASCII_DECI:
                decimal_point = i               #   小数点の位置を取得
    
        return decimal_point
    except Exception as e:
        print("get_decimal_index  error:",e)
        return 0

#   基数を計算する関数(引数:小数点の位置 戻り値:整数部の基数)
def cal_radix(decimal_point:int) -> int:
    radix = 0   #   基数格納変数
    try:
        if (decimal_point - 1) < 0:             #   0より小さければ
            radix = 0                           #   基数は0
        else:                                   #   0以上ならば
            radix = 10 ** (decimal_point - 1)   #   10に小数点の位置から1引いた数を乗算する
        
        return radix
    except Exception as e:
        print("cal_radix error:", e)
        return radix

#   整数部と小数部を分割する関数(引数:bytearyy型配列, 配列サイズ, 小数点の格納位置 戻り値:整数部, 小数部)
def separate_int_deci_part(ary_data:bytearray, ary_size:int, decimal_index:int) -> Tuple[bytearray, bytearray]:
    int_result  = bytearray()   #   整数部格納配列
    deci_result = bytearray()   #   少数部格納配列
    #   分割処理
    try:
        for i in range(ary_size):
            if i < decimal_index:               #   小数点の位置より前ならば
                int_result.append(ary_data[i])  #   整数部の配列に格納
            elif i > decimal_index: #   小数点の位置より後ならば
                deci_result.append(ary_data[i]) #   少数部の配列に格納
    except Exception as e:
        print("sseparate_int_deci_part error:",e)
    return int_result, deci_result

#   bytearrayを数値に変換する関数
def chenge_bytearray_num(ary_data:bytearray, radix):
    ary_size = len(ary_data)    #   配列のサイズを取得
    try:
        for i in range(ary_size):                   
            cal_num = ary_data[i] - ASCII_ZERO      #   ASCIIコードから数値に変換
            if i == 0:                              #   初回なら
                result = cal_num * radix            #   変換値に基数をかけて結果に代入
            else:                                   #   2回目以降なら
                result = result + (cal_num * radix) #   結果に変換値と基数をかけたものを代入
            radix = radix / 10                      #   基数を10で割る
            # print("chenge_bytearray_num; result:", result, " radix:", radix)
        
        return result
    except Exception as e:
        print("chenge_bytearray_num error", e)
        return 0

#   bytearray->float変換関数
def chenge_bytearray_float(ary_data:bytearray, ary_size:int, decimal_point:int, sign:bytes) -> float:
    #   変数宣言
    int_radix   = 0      #   整数部計算用基数
    deci_radix  = 0.1    #   小数部計算用
    int_result  = 0      #   整数部変換結果
    deci_result = 0.1    #   小数部変換結果
    result      = 0.0    #   変換結果(記号あり)

    int_radix = cal_radix(decimal_point)    #   整数部計算用基数算出
    # print("chenge_bytearray_float; int_radix:", int_radix)
    int_ary, deci_ary = separate_int_deci_part(ary_data, ary_size, decimal_point)         #   整数部と小数部に分割
    # print("chenge_bytearray_float; int_ary:", int_ary, " deci_ary:", deci_ary)
    #   bytearray->float変換
    int_result  = chenge_bytearray_num(int_ary, int_radix)  #   整数部変換
    # print("chenge_bytearray_float; int_result:", int_result)
    deci_result = chenge_bytearray_num(deci_ary, deci_radix) #   少数部変換
    # print("chenge_bytearray_float; deci_result:", deci_result)
    result = float(int_result) + deci_result        #   計算結果をまとめる

    #   負の値のとき
    if sign == ASCII_MINUS:
        result = 0 - result                         #   マイナス値に変換

    return result                                   #   計算結果を戻す

#   byte->float型変換関数
def chenge_byte_float(byte_data:bytes):
    try:
        ary_origen = chenge_byte_bytearray(byte_data)   #   bytes型をbytearray型に変換
        # print("chenge_byte_float; ary_origen:", ary_origen)
        ary_origen_size = len(ary_origen)       #   配列サイズを取得
        # print("chenge_byte_float; ary_origen_size", ary_origen_size)
        sign_index, sign = get_sign(ary_origen, ary_origen_size)    #   正負記号と位置を取得
        # print("chenge_byte_float; sign_index:", sign_index, "sign:", sign)
        ary_meas = get_meas(ary_origen, ary_origen_size,sign_index) #   測定値を抽出
        # print("chenge_byte_float; ary_meas:",ary_meas)
        ary_meas_size = len(ary_meas)   #   配列サイズを取得
        meas_decimal_point = get_decimal_index(ary_meas, ary_meas_size) #   小数点の位置を取得
        # print("chenge_byte_float; meas_decimal_point:", meas_decimal_point)
        float_result = chenge_bytearray_float(ary_meas, ary_meas_size, meas_decimal_point, sign)    #   小数点に変換
        return float_result
    except Exception as e:
        print("chenge_byte_float error:", e)
        return 0

def main():
    data_rcv_msg = ''   #   測定データ受信用変数
    ser = serial.Serial(COM, baudrate=2400,parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS,stopbits=serial.STOPBITS_ONE,timeout=5)
    time.sleep(3)
    try:
        data_rcv_msg = get_data(ser, DATA_SND_MSG)
        meas_val = chenge_byte_float(data_rcv_msg)
        print("測定値:", meas_val)
    except Exception as e:
        print("main erorr:", e)
    finally:
        ser.close()


if __name__ == "__main__":
    main()
