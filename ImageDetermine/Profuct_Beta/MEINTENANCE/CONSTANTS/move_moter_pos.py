# 移動用モータの位置を定義する
LEFT_LIMIT      = b'\xbe\n'
WORK_SUPPLY     = b'\xbf\n'
WORK_INSPECTION = b'\xc0\n'
GOOD_WORK       = b'\xc1\n'
BAD_WORK        = b'\xc2\n'
RIGHT_LIMIT     = b'\xc3\n'
#　位置のリスト
MOTOR_POS_LIST = [LEFT_LIMIT, WORK_SUPPLY, WORK_INSPECTION, GOOD_WORK, BAD_WORK, RIGHT_LIMIT]
# 対応するランプの辞書
MOTOR_POS_LAMP_DICT = {
    LEFT_LIMIT      : 0,
    WORK_SUPPLY     : 1,
    WORK_INSPECTION : 2,
    GOOD_WORK       : 3,
    BAD_WORK        : 4,
    RIGHT_LIMIT     : 5
}