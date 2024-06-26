### メインプログラム ###
# DL, ED, PMの三つを走らせ、それぞれの結果をもとに判別を行う

# ライブラリのインポート

# モジュールのインポート
import Dtrmn_DL # ディープラーニング
import Dtrmn_ED # エッジ検出
import Dtrmn_PM # パターンマッチング

# 変数設定
SIZE_IMG = [640, 480] # 全体で使用する画像サイズ

'''
Some things to do:
'''

# 適切な範囲に切り取る
def cut_image():
    # 画像を切り取る処理
    print("cut_image")

# PLCからの信号を受け取る
def get_signal():
    # PLCからの信号を受け取る処理
    print("get_signal")

# 重み付き投票
def weighted_vote():
    # 重み付き投票の処理
    print("weighted_vote")

# メイン処理
def main():
        ### 画像処理開始 ###
        # カメラ画像を取得
        # 適切な範囲に切り取る
        cut_image()  # 画像を切り取る処理
        # 画像をSIZE_IMGにリサイズ

        # ディープラーニング
        
        # エッジ検出

        # パターンマッチング

        # 判別
        #それぞれの結果から、重み付き投票を行い、判別
        weighted_vote()


if __name__ == "__main__":
    while True:
        if get_signal(): # カメラが新しく画像を取得したら、もしくはPLCから信号が来たら画像処理
            main()  # メイン処理
        else:
            pass    # 何もしない