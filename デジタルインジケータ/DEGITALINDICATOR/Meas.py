from typing import Tuple, Optional

class ConversionHandler:
    ASCII_DECIMAL = 46
    ASCII_ZERO = 48
    ASCII_NINE = 57
    ASCII_PLUS = 43
    ASCII_MINUS = 45
    ASCII_R = 13

class DataProcessor(ConversionHandler):
    @staticmethod
    def search_sign(base_bytearray: bytearray) -> Tuple[int, int]:
        # bytearrayを分割
        for index, byte in enumerate(base_bytearray):
            # byteの中に[+],[-]が存在すればそれを返す
            if byte in (ConversionHandler.ASCII_PLUS, ConversionHandler.ASCII_MINUS):
                return byte, index
        return 0, -1
    
    @staticmethod
    def delete_cr(base_bytearray: bytearray) -> bytearray:
        cr_delete_array = bytearray()
        for byte in base_bytearray:
            # [R]より前の配列を返す
            if byte == ConversionHandler.ASCII_R:
                return cr_delete_array
            else:
                cr_delete_array.append(byte)
        return cr_delete_array

    @staticmethod
    def extraction_meas(base_bytearray: bytearray, sign_index: int) -> bytearray:
        # 引数+1が配列の長さより短かったら
        if sign_index + 1 < len(base_bytearray):
            # 引数+1の位置のデータを返す
            return base_bytearray[sign_index + 1:]
        return bytearray()

    @staticmethod
    def confim_bytearray_number(base_bytearray: bytearray) -> int:
        for byte in base_bytearray:
            # [.]ではない
            if byte != ConversionHandler.ASCII_DECIMAL:
                # [0～9]ではない
                if ConversionHandler.ASCII_ZERO > byte or byte > ConversionHandler.ASCII_NINE:
                    return -1
        return 1

class MeasurementConverter(ConversionHandler):
    @staticmethod
    def search_decimal_index(base_bytearray: bytearray) -> int:        
        for index, byte in enumerate(base_bytearray):
            # [.]の位置を返す
            if byte == ConversionHandler.ASCII_DECIMAL:
                return index
        return -1

    # ?
    @staticmethod
    def calculate_radix(decimal_index: int) -> int:
        if decimal_index - 1 >= 0:
            return 10 ** (decimal_index - 1)
        else:
            return -1

    @staticmethod
    def divide_bytearray(base_bytearray: bytearray, decimal_index: int) -> Tuple[bytearray, bytearray]:
        # 整数
        integer_part = base_bytearray[:decimal_index]
        # 小数点以下
        float_part = base_bytearray[decimal_index + 1:]
        return integer_part + float_part

    @staticmethod
    def conversion_bytearray_float(base_bytearray: bytearray, place_value: float) -> float:
        converted_value = 0.0
        for byte in base_bytearray:
            # ASCCIコードを数値に直して 引数をかけた物を加算している
            converted_value += ((byte - ConversionHandler.ASCII_ZERO) * place_value)
            # 引数を/10 基数を1下げる
            place_value /= 10
        return converted_value

    def convertion_meas_float(self, base_array: bytearray) -> Optional[float]:
        # インスタンス化
        processor = DataProcessor()
        # [R]を削除
        delete_cr_array = processor.delete_cr(base_array)
        # [+],[-]を探してその位置を返す
        sign, sign_index = processor.search_sign(delete_cr_array)
        if sign_index == -1:
            return None
        # [+],[-]符号よりあと(測定値)を分割
        meas_array = processor.extraction_meas(delete_cr_array, sign_index)
        if not meas_array:
            return None
        # 測定値がバッグてないかチェック
        result = processor.confim_bytearray_number(meas_array)
        if result == -1:
            return None
        # 小数点の位置を探して返す
        decimal_index = self.search_decimal_index(meas_array)
        if decimal_index == -1:
            return None
        # 小数点の位置から基数を求める
        place_value = self.calculate_radix(decimal_index)
        if place_value == -1:
            return None
        # 測定値から[.]を抜いてそれ以外を結合
        meas_part = self.divide_bytearray(meas_array, decimal_index)
        # ASCIIコードをfloat型に変換
        meas_value = self.conversion_bytearray_float(meas_part, place_value)
        # 符号が[-]の場合
        if sign == ConversionHandler.ASCII_MINUS:
            meas_value = meas_value * -1
        return meas_value

    # エラーに種類判別
    def judge_error(self, base_array: bytearray) -> float:
        if len(base_array) > 2:
            if base_array[2] == 49:
                return -101.0
            else:
                return -102.0
        else:
            return -102.0

    # エラーが
    def convertion_byte_float(self, byte: bytes) -> float:
        origen_array = bytearray(byte)
        if (origen_array[0], origen_array[1]) == (57, 49):
            return self.judge_error(origen_array)
        else:
            return self.convertion_meas_float(origen_array)

if __name__ == "__main__":
    test_data = {
        b"01A+000.0101\r",
        b"01A+001.0800\r",
        b"01A+014.9000\r",
        b"01A+123.1110\r",
        b"911\r",
        b"912\r"
    }
    test = MeasurementConverter()
    for data in test_data:
        result = test.convertion_byte_float(data)
        print(f"変換前:{data}")
        print(f"変換後:{result}")

    