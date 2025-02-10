# PC-PLC間通信コマンド変換
# 命令を変換する
from MEINTENANCE.CONSTANTS.command  import *
PUSH_COMMAND = {
    SOLENOID            : ("ソレノイド動作コマンド", "外観検査部"),
    STEPING             : ("ステッピングモータ回転", "外観検査部"),
    CYLINDER_UP_START   : ("シリンダ前進コマンド", "移載部"),
    CYLINDER_DOWN_START : ("シリンダ後退コマンド", "移載部")
}
HOLD_DOWN_COMMAND = {
    MOTOR_NOMAL         : ("移動用モータ正転コマンド", "移載部"),
    MOTOR_REVERSE       : ("移動用モータ逆転コマンド", "移載部"),
    HOLD_END            : ("モータ停止コマンド", "移載部")
}
ADSORPTION_COMMAND = {
    ADSORPTION_ON       : ("吸着開始コマンド", "移載部"),
    ADSORPTION_OFF      : ("吸着終了コマンド", "移載部")
}