# PROJECT

このプロジェクトはPLCとのコマンドのやり取りを目的としたシリアル通信の管理ツールです。

## セットアップ方法

1. 依存関係のインストール:
   ```bash
   pip install -r requirements.txt


## フォルダの構成
## シリアル通信関係
├── SERIAL/
│   ├── constant/    # 定数やEnum型を格納
│   ├── dict/        # 自作辞書を格納
│   ├── logs/        # デバック・エラーログを格納
│   ├── manager/     # シリアル通信を行う関数群
│   └── test/        # 単体テストや結合テスト
├── UTILS/           # ユーティリティ関数
├── requirements.txt # 依存関係
└── README.md        # プロジェクト説明

## 使い方

