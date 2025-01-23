# PC-PLC間通信コマンド変換
# 命令を変換する
from MEINTENANCE.CONSTANTS.command  import *
PUSH_COMMAND = {
    SOLENOID            : "ソレノイド動作コマンドのキー",
    STEPING             : "ステッピングモータ回転コマンドのキー",
    CYLINDER_UP_START   : "シリンダ前進のコマンドのキー",
    CYLINDER_DOWN_START : "シリンダ後退のコマンドのキー"
}
HOLD_DOWN_COMMAND = {
    MOTOR_NOMAL         : "移動用モータ正転のコマンドのキー",
    MOTOR_REVERSE       : "移動用モータ逆転のコマンドのキー"
}
ADSORPTION_COMMAND = {
    ADSORPTION_ON       : ("吸着開始のコマンドのキー", "移載部"),
    ADSORPTION_OFF      : ("吸着終了のコマンドのキー", "移載部")
}