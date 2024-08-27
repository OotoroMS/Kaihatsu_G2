import numpy as np
import cv2
import glob
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
import tensorflow as tf

# 繝�繝舌ャ繧ｰ逕ｨ險ｭ螳�
tf.config.run_functions_eagerly(True)

# 蟄ｦ鄙偵ョ繝ｼ繧ｿ縺ｮ隱ｭ縺ｿ霎ｼ縺ｿ
def load_images(path):
    images = []
    for file in glob.glob(path + '/*.jpg'):
        image = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        image = image[625:625+1024, 0:2592]  # 逕ｻ蜒上�ｮ蛻�繧雁叙繧�
        sobel_image = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)  # Sobel繝輔ぅ繝ｫ繧ｿ縺ｮ驕ｩ逕ｨ
        sobel_image = np.absolute(sobel_image)
        sobel_image = np.uint8(sobel_image)
        sobel_image = cv2.resize(sobel_image, (512, 256))  # 逕ｻ蜒上�ｮ繝ｪ繧ｵ繧､繧ｺ
        sobel_image = sobel_image.astype('float32') / 255.
        images.append(sobel_image)
        # 繝�繝舌ャ繧ｰ逕ｨ�ｼ壼推逕ｻ蜒上�ｮ蠖｢迥ｶ繧貞�ｺ蜉�
        print(f'Loaded image shape: {sobel_image.shape}')
    return np.array(images)

X_train = load_images('ImageDetermine/Test_Alpha/Images/Training')

# 繝�繝舌ャ繧ｰ逕ｨ�ｼ夊ｪｭ縺ｿ霎ｼ繧薙□繝�繝ｼ繧ｿ縺ｮ蠖｢迥ｶ繧貞�ｺ蜉�
print(f'Training data shape: {X_train.shape}')

X_train = X_train.reshape(-1, 256, 512, 1)

# AutoEncoder繝｢繝�繝ｫ縺ｮ讒狗ｯ�
input_img = Input(shape=(256, 512, 1))

# 繧ｨ繝ｳ繧ｳ繝ｼ繝驛ｨ蛻�
x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
x = MaxPooling2D((2, 2), padding='same')(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2), padding='same')(x)

# 繝�繧ｳ繝ｼ繝驛ｨ蛻�
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
x = Conv2D(32, (3, 3), activation='relu', padding='same')(x)
x = UpSampling2D((2, 2))(x)
decoded = Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy', run_eagerly=True)

# 繝�繝舌ャ繧ｰ逕ｨ�ｼ壹Δ繝�繝ｫ縺ｮ繧ｵ繝槭Μ繝ｼ繧貞�ｺ蜉�
autoencoder.summary()

# 繝｢繝�繝ｫ縺ｮ蟄ｦ鄙�
autoencoder.fit(X_train, X_train, epochs=50, batch_size=8, shuffle=True)  # 繝舌ャ繝√し繧､繧ｺ繧貞ｰ上＆縺�

# 繝｢繝�繝ｫ縺ｮ菫晏ｭ�
autoencoder.save('autoencoder_model.h5')
