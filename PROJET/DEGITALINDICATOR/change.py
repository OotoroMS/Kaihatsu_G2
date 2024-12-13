from typing import Tuple, Optional

class ConversionHandler:
    ASCII_DECIMAL = 46
    ASCII_ZERO = 48
    ASCII_NINE = 57
    ASCII_PLUS = 43
    ASCII_MINUS = 45
    ASCII_CR = 13

class DataProcessor(ConversionHandler):
    @staticmethod
    def search_sign(base_bytearray: bytearray) -> Tuple[Optional[int], int]:
        for index, byte in enumerate(base_bytearray):
            if byte in (ConversionHandler.ASCII_PLUS, ConversionHandler.ASCII_MINUS):
                return byte, index
        return None, -1

    @staticmethod
    def delete_cr(base_bytearray: bytearray) -> bytearray:
        cr_delete_array = bytearray()
        for byte in base_bytearray:
            if byte == ConversionHandler.ASCII_CR:
                return cr_delete_array
            else:
                cr_delete_array.append(byte)
        return cr_delete_array

    @staticmethod
    def extraction_meas(base_bytearray: bytearray, sign_index: int) -> bytearray:
        if sign_index + 1 < len(base_bytearray):
            return base_bytearray[sign_index + 1:]
        return bytearray()

    @staticmethod
    def confim_bytearray_number(base_bytearray: bytearray) -> bool:
        for byte in base_bytearray:
            if byte != ConversionHandler.ASCII_DECIMAL and not (
                ConversionHandler.ASCII_ZERO <= byte <= ConversionHandler.ASCII_NINE):
                return False
        return True

class MeasurementConverter(ConversionHandler):
    @staticmethod
    def search_decimal_index(base_bytearray: bytearray) -> int:
        for index, byte in enumerate(base_bytearray):
            if byte == ConversionHandler.ASCII_DECIMAL:
                return index
        return -1

    @staticmethod
    def calculate_radix(decimal_index: int) -> int:
        if decimal_index - 1 >= 0:
            return 10 ** (decimal_index - 1)
        else:
            return -1

    @staticmethod
    def divide_bytearray(base_bytearray: bytearray, decimal_index: int) -> Tuple[bytearray, bytearray]:
        integer_bytearray = base_bytearray[:decimal_index]
        decimal_bytearray = base_bytearray[decimal_index + 1:]
        return integer_bytearray, decimal_bytearray

    @staticmethod
    def conversion_bytearray_float(base_bytearray: bytearray, place_value: float) -> float:
        converted_value = 0.0
        for byte in base_bytearray:
            converted_value += ((byte - ConversionHandler.ASCII_ZERO) * place_value)
            place_value /= 10
        return converted_value

    def convertion_meas_float(self, base_array: bytearray) -> Optional[float]:
        processor = DataProcessor()
        sign, meas_array = processor.search_sign(base_array)
        delete_cr_array = processor.delete_cr(base_array)
        meas_array = processor.extraction_meas(delete_cr_array, sign_index=0)
        if meas_array and processor.confim_bytearray_number(meas_array):
            decimal_index = self.search_decimal_index(meas_array)
            place_value = self.calculate_radix(decimal_index)
            if place_value > -1:
                intger_array, decimal_array = self.divide_bytearray(meas_array, decimal_index)
                intger_value = self.conversion_bytearray_float(intger_array, place_value)
                decimal_value = self.conversion_bytearray_float(decimal_array, 0.1)
                convertion_result = intger_value + decimal_value
                if sign == ConversionHandler.ASCII_MINUS:
                    convertion_result = -convertion_result
                return convertion_result
        return None

    def judge_error(self, base_array: bytearray) -> float:
        if len(base_array) > 2:
            if base_array[2] == 49:
                return -101.0
            else:
                return -102.0
        else:
            return -102.0

    def convertion_byte_float(self, byte: bytes) -> float:
        origen_array = bytearray(byte)
        if (origen_array[0], origen_array[1]) == (57, 49):
            return self.judge_error(origen_array)
        else:
            return self.convertion_meas_float(origen_array)
