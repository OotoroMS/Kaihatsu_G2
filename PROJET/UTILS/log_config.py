# /UTILS/log_config.py

import logging
from logging.handlers import TimedRotatingFileHandler

# ログ設定
def setup_logging():
    # ロガーを作成
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # ロガーの最低レベルをDEBUGに設定

    # 共通のフォーマット
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # エラーログ用のハンドラを作成（7日ごとにローテーション）
    error_handler = TimedRotatingFileHandler(
        'PROJET/SERIAL/logs/error_log.txt', 
        when='midnight',  # 毎日0時にローテーション
        interval=1,  # 1日ごとにローテーション
        backupCount=7,  # ログを7日分保持
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)  # エラーログ用のレベルをERRORに設定
    error_formatter = logging.Formatter(log_format)
    error_handler.setFormatter(error_formatter)

    # デバッグログ用のハンドラを作成（7日ごとにローテーション）
    debug_handler = TimedRotatingFileHandler(
        'PROJET/SERIAL/logs/debug_log.txt',
        when='midnight',  # 毎日0時にローテーション
        interval=1,  # 1日ごとにローテーション
        backupCount=7,  # ログを7日分保持
        encoding='utf-8'
    )
    debug_handler.setLevel(logging.DEBUG)  # デバッグログ用のレベルをDEBUGに設定
    debug_formatter = logging.Formatter(log_format)
    debug_handler.setFormatter(debug_formatter)

    # ハンドラをロガーに追加
    logger.addHandler(error_handler)
    logger.addHandler(debug_handler)

    # ロガーの利用
    return logger

