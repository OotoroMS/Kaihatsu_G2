import cv2
import os
from Dtrmn_DL import is_scratch_image

def cut_image(img, x, y, w, h):
    height, width = img.shape[:2]
    x = max(0, min(x, width))
    y = max(0, min(y, height))
    w = min(w, width - x)
    h = min(h, height - y)
    return img[y:y+h, x:x+w]

# メイン処理
def main():
    # アプローチの選択
    print("Select the approach for inference:")
    print("2: Resize image to 1296x512")
    print("3: Split image into 512x512 patches")
    approach = input("Enter the approach number (2 or 3): ")

    if approach == '2':
        model_name = 'autoencoder_model_1296x512.h5'
    elif approach == '3':
        model_name = 'autoencoder_model_512x512.h5'
    else:
        print("Invalid selection. Exiting.")
        return

    # 画像処理開始
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

    prev_image = None
    prev_image_path = 'ImageDetermine/Test_Alpha/prev_image.jpg'
    if os.path.exists(prev_image_path):
        prev_image = cv2.imread(prev_image_path)

    while True:
        ret, current_image = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        height, width = current_image.shape[:2]
        print(f"Captured image resolution: {width}x{height}")

        # 画像のクロップ
        x, y, w, h = 0, 625, 2592, 1024
        tmp_img = cut_image(current_image, x, y, w, h)

        if approach == '2':
            # 画像を1/2にリサイズ (1296x512)
            resized_img = cv2.resize(tmp_img, (1296, 512))

            # 一時ファイルとして画像を保存
            tmp_img_path = 'tmp_img.jpg'
            cv2.imwrite(tmp_img_path, resized_img)

            # 画像の傷の判別を行う
            is_scratch = is_scratch_image(tmp_img_path, model_name)
        
        elif approach == '3':
            # 画像を512x512のパッチに分割して処理
            patches = split_image_into_patches(tmp_img, patch_size=(512, 512))
            is_scratch = any(is_scratch_image(patch, model_name) for patch in patches)

        print(f'Scratch detected: {is_scratch}')

        # 画像をリサイズして表示
        display_image = cv2.resize(tmp_img, (int(w/2), int(h/2)))
        cv2.imshow("Result", display_image)

        prev_image = current_image.copy()
        cv2.imwrite(prev_image_path, prev_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def split_image_into_patches(image, patch_size=(512, 512)):
    patches = []
    img_height, img_width = image.shape[:2]
    for y in range(0, img_height, patch_size[1]):
        for x in range(0, img_width, patch_size[0]):
            patch = image[y:y+patch_size[1], x:x+patch_size[0]]
            if patch.shape[:2] == patch_size:
                patches.append(patch)
    return patches

if __name__ == "__main__":
    main()
