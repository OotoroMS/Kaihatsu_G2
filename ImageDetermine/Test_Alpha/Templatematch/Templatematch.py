import cv2
import numpy as np
from matplotlib import pyplot as plt

# メイン画像とテンプレート画像をグレースケールで読み込む
img_path = 'Z:/G2kaihatu/VSCode/tenpure/jpg/DSC_0398.jpg'  # メイン画像のパス
template_path = 'Z:/G2kaihatu/VSCode/tenpure/jpg/DSC_0398Template.jpg'  # テンプレート画像のパス

# メイン画像を読み込む
img = cv2.imread(img_path, 0)
if img is None:
    raise FileNotFoundError(f"メイン画像が見つかりません。パスを確認してください: {img_path}")

# テンプレート画像を読み込む
template = cv2.imread(template_path, 0)
if template is None:
    raise FileNotFoundError(f"テンプレート画像が見つかりません。パスを確認してください: {template_path}")

# テンプレート画像の幅と高さを取得
w, h = template.shape[::-1]

# テンプレートマッチングのためにメイン画像をコピー
img2 = img.copy()

# 比較する6つのテンプレートマッチング手法のリスト
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# 各手法を試す
for meth in methods:
    img = img2.copy()  # 元の画像を再度コピーしてリセットする
    method = eval(meth)  # 文字列を対応する関数に変換する

    # テンプレートマッチングを適用する
    res = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # マッチ結果の最小値、最大値、およびそれらの位置を取得

    # TM_SQDIFF または TM_SQDIFF_NORMEDの場合は最小値を使用する
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)  # テンプレートの位置の右下の座標を計算する

    # マッチした領域を矩形で囲む
    cv2.rectangle(img, top_left, bottom_right, 255, 2)

    # 結果を表示する
    plt.subplot(121), plt.imshow(res, cmap='gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    # グラフを表示する
    plt.show()