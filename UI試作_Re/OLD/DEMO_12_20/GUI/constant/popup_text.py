# TextPopupに表示するメッセージを登録する(今後関係ないものは独立させる)
from GUI.constant.popup_name import *
POPUP_TEXTS = {
    NONE_DATA    : "データが存在しません",
    DB_RESET     : "データベースを初期化しました",
    END_POPUP    : "終了しますか?",
    INDICATOR_OK : "更新しました",
    INDICATOR_NG : "更新に失敗しました",
    PASS_POPUP1  : "パスワードが違います",
    PASS_POPUP2  : "もう一度入力してください",
    PASS_POPUP3  : "最初からやり直してください",
    SPASS_POPUP  : "パスワードを変更しました",
    RPASS_POPUP  : "パスワードを入力してください",
    RESET_ASK    : "データベースをリセットしますか？",
    ERROR_POPUP  : "エラーが発生しました",
    ACTIVE_PASS  : "装置を停止してください"
}