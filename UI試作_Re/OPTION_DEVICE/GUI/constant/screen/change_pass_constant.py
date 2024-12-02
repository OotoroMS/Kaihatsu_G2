from GUI.constant.file_path import *

QUERY = "UPDATE pass_num SET num = "

PASS_TITLE_STATUS  = {
    "coordinate" : (0,   0),
    "size"       : (600, 200),
    "image_path" : TITLE_FILE_PATH + "title_change_pass.png"
}
NEW_PASSWORD_EXPTXT_STAUTS = {
    "coordinate" : (590, 40),
    "size"       : (850, 200),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_new_pass.png"
}
RETRY_PASSWORD_EXPTXT_STATUS = {
    "coordinate" : (635, 40),
    "size"       : (850, 200),
    "image_path" : EXPTXT_FILE_PATH + "exptxt_retry_pass.png"
}
NEW   = "new"
RETRY = "retry"
TITLE = 0