### メインプログラム ###
# DL, ED, PMの三つを走らせ、それぞれの結果をもとに判別を行う

# ライブラリのインポート
import cv2 # OpenCV

# モジュールのインポート
import Dtrmn_DL # ディープラーニング
import Dtrmn_ED # エッジ検出
import Dtrmn_TM # テンプレートマッチング

# 変数設定
SIZE_IMG = [640, 480] # 全体で使用する画像サイズ？

# 関数の設定

# 適切な範囲に切り取る
def cut_image():
    # 画像を切り取る処理
    print("cut_image")

# PLCからの信号を受け取る
def get_signal():
    # PLCからの信号を受け取る処理
    print("get_signal")
    return True

# 重み付き投票
def weighted_vote():
    # 重み付き投票の処理
    print("weighted_vote")

# メイン処理
def main():
        ### 画像処理開始 ###
        ## 画像取得
        # カメラを取得
        cap = cv2.VideoCapture(0)
        # カメラ画像を取得
        ret, current_image = cap.read()
        ## テストで表示
        cv2.imshow("current_image", current_image)
        cv2.waitKey(0)
        # 適切な範囲に切り取る
        tmp_img = cut_image(current_image)  # 画像を切り取る処理


        ## 画像処理
        #結果リストの初期化
        results = [] # 結果リストの長さは3
        
        # ディープラーニング
        dl = Dtrmn_DL.DeepLearning() #クラスをインスタンス化
        results[0] = dl.determine(tmp_img) # ディープラーニングで判別
        
        # エッジ検出
        ed = Dtrmn_ED.EdgeDetection() #クラスをインスタンス化
        results[1] = ed.determine(tmp_img) # エッジ検出で判別

        # テンプレートマッチング
        tm = Dtrmn_TM.TemplateMatching() #クラスをインスタンス化
        results[2] = tm.determine(tmp_img) # テンプレートマッチングで判別

        ## 判別
        #それぞれの結果から、重み付き投票を行い、判別
        weighted_vote()


if __name__ == "__main__":
    while True:
        if get_signal(): # カメラが新しく画像を取得したら、もしくはPLCから信号が来たら画像処理
            main()  # メイン処理
        else:
            pass    # 何もしない