# PROJECT

このプロジェクトはPLCとのコマンドのやり取りを目的としたシリアル通信の管理ツールです。

## セットアップ方法

1. 依存関係のインストール:
   ```bash
   pip install -r requirements.txt


## フォルダの構成
PROJECT/
├── DATABASE/
├── DEGITALINDICATOR/
├── GUI/
│   ├── BACK/     # 表示画面のデータ処理を担当(例:シリアル通信やデータベースへの接続等)
│   ├── FRONT/    # 表示画面の表示を担当 
│   │   ├── constant/      # 定数やEnum型を格納
│   │   ├── image/         # 画像を格納
│   │   ├── parts/         # ボタン・テキストの作成など汎用クラスの格納
│   │   ├── popup/         # ポップアップの表示の作成(Baseを親にして子を作成)
│   │   ├── screen/        # スクリーンの表示の作成(Baseを親にして子を作成)
│   │   ├── Application.py # 各描画処理やイベント処理,BACKとのやり取り等を行う
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

