from type_check import type_check_decorator

class Test:
    # 型チェックデコレータを個別にテスト
    @type_check_decorator({'data': bytes})
    def test_function(self, data: bytes):
        print(f"Received data type: {type(data).__name__}")

test = Test()
test.test_function(b'\x01\x8e')
