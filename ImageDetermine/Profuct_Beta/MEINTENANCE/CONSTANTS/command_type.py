# 処理識別用定数
OPERATION_STATUS    = "OPERATION_STATUS"
HOLD_DOWN_START     = "PRESS_START"
HOLD_DOWN_END       = "PLESS_END"
WORK_STATUS         = "WORK_STATUS"
CHANGE_PASS         = "CHANGE_PASS"
ADSORPTION          = "ADSORPTION"
HOLD_DOWN           = "HOLD_DOWN"
PASSWORD            = "PASSWORD"
DB_RESET            = "DB_RESET"
LIGHT              = "LIGHT"
PLC                 = "plc"

# PLC->PCの処理識別用
PLC_PC_MESSAGE = "plc_pc_message"
# PC->PLCの返答
PC_PLC_RESPONSE = "pc_plc_response"
# データベース更新の返答
DB_RESPONSE = "db_response"
# ランプ動作用
RUN     = "RUN"
FINISH  = "FINISH"
ERROR   = "ERROR"
# アプリ終了用
APP_END = "APP_END"
# パスワード更新
UPDATE_PASS = "_pass_"
# 更新及び処理に成功
SUCCESS = "SUCCESS"
# メンテナンスモードに移行
MODE_MEINTENANCE = ["動作確認モード", "動作確認部"]
# 主動作モードに移行
MODE_MAIN = ["主動作モード",   "動作確認部"]
# 動作完了
MODE_FINISH = "動作完了"
# モータ励磁完了
MOTOR_ON = ["ステッピング励磁完了", "外観検査部"]