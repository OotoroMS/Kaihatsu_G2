# /UTILS/log_config.py

import logging
from logging.handlers import TimedRotatingFileHandler

# ログ設定
def setup_logging():
    logger = logging.getLogger(__name__)

    # すでにハンドラが設定されている場合は追加しない
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
        
        # エラーログ用のハンドラ
        error_handler = TimedRotatingFileHandler(
            'PROJET/SERIAL/logs/error_log.txt',
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(log_format)
        error_handler.setFormatter(error_formatter)
        
        # デバッグログ用のハンドラ
        debug_handler = TimedRotatingFileHandler(
            'PROJET/SERIAL/logs/debug_log.txt',
            when='midnight',
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_formatter = logging.Formatter(log_format)
        debug_handler.setFormatter(debug_formatter)
        
        # ハンドラをロガーに追加
        logger.addHandler(error_handler)
        logger.addHandler(debug_handler)

    return logger

