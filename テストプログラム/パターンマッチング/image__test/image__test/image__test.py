#   パターンマッチング
import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    #   対象画像読み込み
    target_img = cv2.imread(".\\test_image\\IMG_6206.jpeg")
    #   テンプレート画像読み込み
    temp_img = cv2.imread(".\\test_image\\DSC_target3.jpg")
    print("画像準備OK")

    target_img_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
    temp_img_gray = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)


    #   パターンマッチング
    res = cv2.matchTemplate(target_img_gray, temp_img_gray, cv2.TM_CCOEFF_NORMED)

   

    threshold = 0.7

    loc = np.where(res >= threshold)

    #   検出対象画像サイズ
    w = temp_img.shape[1]
    h = temp_img.shape[0]

    #   テスト用画像をコピー(確認用画像生成)
    dst = target_img.copy()

    #   マッチした箇所に赤枠を描写
    #   赤枠の右下の座標は左上の座標に検出対象画像の幅、高さを足す
    for x,y in zip(*loc[::-1]):
        cv2.rectangle(dst,  (x,y),  (x+w,y+h),  (0,0,225),2)

    plt.imshow(cv2.cvtColor(dst,cv2.COLOR_BGR2RGB))
    plt.show()
    print("完了")

main()
if __name__ == "__main___":
    print("ok2")
    main()