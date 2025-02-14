# PLC-PC返答
from MEINTENANCE.CONSTANTS.command  import *
PUSH_RESULT = {
    SOLENOID            : ["ソレノイド動作完了",         "外観検査部"],
    STEPING             : ["ステッピングモータ回転完了", "外観検査部"],
    CYLINDER_UP_START   : ["シリンダ前進完了",           "移載部"],
    CYLINDER_DOWN_START : ["シリンダ後退完了",           "移載部"]
}
ADSORPTION_RESULT = {
    ADSORPTION_ON       : ["吸着ON",         "移載部"],
    ADSORPTION_OFF      : ["吸着OFF",        "移載部"]
}
LIGHT_RESULT = {
    LIGHT_ON            : ["照明ON",         "外観検査部"],
    LIGHT_OFF           : ["照明OFF",        "外観検査部"]
}