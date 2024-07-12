import os
import cv2
import Dtrmn_DL  # ディープラーニング
import Dtrmn_ED  # エッジ検出
import Dtrmn_TM  # テンプレートマッチング

# 関数の設定

# 適切な範囲に切り取る
def cut_image(img, x, y, w, h):
    # 画像の範囲外にならないように調整
    height, width = img.shape[:2]
    x = max(0, min(x, width))
    y = max(0, min(y, height))
    w = min(w, width - x)
    h = min(h, height - y)
    return img[y:y+h, x:x+w]

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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

    # 前回の画像を読み込む（初回はNone）
    prev_image = None
    prev_image_path = 'ImageDetermine/Test_Alpha/prev_image.jpg'
    if os.path.exists(prev_image_path):
        prev_image = cv2.imread(prev_image_path)

    while True:
        # カメラから画像を取得
        ret, current_image = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # 解像度を表示
        height, width = current_image.shape[:2]
        print(f"Captured image resolution: {width}x{height}")

        # 適切な範囲に切り取る
        x, y, w, h = 0, 625, 2592, 1024  # 切り取る範囲を指定
        tmp_img = cut_image(current_image, x, y, w, h)  # 画像を切り取る処理

        '''
        # 変化があった領域を検出
        if prev_image is not None:
            prev_img_cropped = cut_image(prev_image, x, y, w, h)  # 前回の画像も同じ範囲で切り取る
            processed_image, change_detected = Dtrmn_DL.detect_changes(prev_img_cropped, tmp_img)
            if change_detected:
                # 変化があった場合にのみYOLOで詳細な画像処理を行う
                processed_image = Dtrmn_DL.DeepLearning().determine(processed_image)
        else:
            processed_image = tmp_img
        '''

        #とりあえず毎回正直にDLを通す
        processed_image = Dtrmn_DL.DeepLearning().determine(tmp_img)

        # 画像をリサイズして表示
        display_image = cv2.resize(processed_image, (int(w/2), int(h/2)))
        cv2.imshow("Result", display_image)

        # 現在の画像を保存
        prev_image = current_image.copy()
        cv2.imwrite(prev_image_path, prev_image)

        # 'q'キーが押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # カメラを解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
