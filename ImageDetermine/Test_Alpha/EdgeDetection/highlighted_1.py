import cv2
import matplotlib.pyplot as plt
import numpy as np

def detect_rings(image_path, param1=50, param2=30, minRadius=20, maxRadius=150):
    # 画像をグレースケールで読み込む
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"Error: Image at path {image_path} could not be loaded.")
        return
    else:
        print(f"Image loaded successfully from {image_path}")

    # Sobelフィルタを適用してエッジ検出を行う
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)  # x方向のエッジ検出
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)  # y方向のエッジ検出

    # 各方向の勾配強度を合成して勾配の強度を計算する
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

    # 勾配の強度を0から255の範囲にスケーリングする
    gradient_magnitude_scaled = cv2.normalize(gradient_magnitude, None, 0, 235, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # 二値化
    _, binary_image = cv2.threshold(gradient_magnitude_scaled, 50, 255, cv2.THRESH_BINARY)

    # 輪郭を検出
    contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # オリジナルの画像をカラーで読み込み、円を描画する
    image_color = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # 検出された輪郭をフィルタリングして円形の輪を検出
    for contour in contours:
        # 輪郭を囲む最小の外接円を取得
        ((x, y), radius) = cv2.minEnclosingCircle(contour)
        # 円形の輪として認識されるために、輪郭の周囲のアスペクト比を確認
        if 20 < radius < 150:
            cv2.circle(image_color, (int(x), int(y)), int(radius), (0, 0, 255), 2)

    # Matplotlibを使用して結果を表示する
    plt.figure(figsize=(18, 6))

    # 元の画像を表示
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    # Sobelエッジ検出結果を表示
    plt.subplot(1, 3, 2)
    plt.imshow(gradient_magnitude_scaled, cmap='gray')
    plt.title('Sobel Edge Detection')
    plt.axis('off')

    # 輪が描かれた画像を表示
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB))
    plt.title('Detected Rings')
    plt.axis('off')

    plt.show()

# 画像のパスを指定
image_path = 'Z:/G2kaihatu/VSCode/DSC_0398.jpg'

# detect_rings関数を実行
detect_rings(image_path, param1=100, param2=50, minRadius=20, maxRadius=150)
# param1:Cannyエッジ検出の上限閾値
# param2:必要な投票数
# minRadius:最小半径  maxRadius:最大半径