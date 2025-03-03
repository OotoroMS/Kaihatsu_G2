OPERATION_ACTIVE = "稼働中"
OPERATION_STOP   = "停止中"
OPERATION_ERROR  = "エラー"
OPERATION_ERROR_BYTES  = {
    b'\xe6\n', b'\xe7\n', b'\xe8\n', b'\xe9\n', b'\xea\n', b'\xeb\n', b'\xec\n', b'\xed\n', b'\xee\n', b'\xef\n',
    b'\\n', b'\xf1\n', b'\xf2\n', b'\xf3\n', b'\xf4\n', b'\xf5\n', b'\xf6\n', b'\xf7\n', b'\xf8\n', b'\xf9\n'
}
OPERATION_STOP_BYTES = {
    b'\xfa\n', b'\xfb\n', b'\xfc\n', b'\xfd\n'
}