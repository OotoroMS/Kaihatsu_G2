class SerialDataFormatter:
    @staticmethod
    def format_send(byte: bytes):
        if byte is not None:
            return b'\x00\x01' + byte + b'\r\n'
        print("Cannot format None to bytes")
        return None
