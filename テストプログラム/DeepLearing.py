# Data�t�H���_���̃f�[�^��ǂݍ��݁A�摜���ʂŃL�Y���擾����

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.layers import Flatten, Dense, Dropout
from keras.models import Model


# ���f�������Ƃɔ��ʂ���N���X
class ImageDiscrimination:
    def __init__(self):
        self.model = load_model('model.h5')
    
    def predict(self, img):
        # ���f���̓ǂݍ���
        model = load_model('model.h5')

        # �t�H���_�����ׂẲ摜�̓ǂݍ���
        path = 'Data/'
        files = os.listdir(path)
        for file in files:
            img = image.load_img(path + file, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            # �摜�̔���
            preds = model.predict(x)
            if preds[0][0] > preds[0][1]:
                print(file + '�̓L�Y������܂�')
            else:
                print(file + '�̓L�Y������܂���')

# ���f�����쐬����N���X
class ModelCreate:
    def __init__(self):
        self.model = self.create_model()
    
    def create_model(self):
        # ���O�w�K�ς݂�VGG16��ǂݍ���
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

        # �S�����w��ǉ�
        top_model = base_model.output
        top_model = Flatten()(top_model)
        top_model = Dense(256, activation='relu')(top_model)
        top_model = Dropout(0.5)(top_model)
        top_model = Dense(2, activation='softmax')(top_model)

        # ���f��������
        model = Model(inputs=base_model.input, outputs=top_model)

        # VGG16�̏d�݂��Œ�
        for layer in base_model.layers:
            layer.trainable = False

        # ���f�����R���p�C��
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        return model

    def train(self):
        # �f�[�^�̓ǂݍ���
        train_data = np.load('train_data.npy')
        train_label = np.load('train_label.npy')
        test_data = np.load('test_data.npy')
        test_label = np.load('test_label.npy')

        # ���f���̊w�K
        self.model.fit(train_data, train_label, batch_size=32, epochs=10, verbose=1, validation_data=(test_data, test_label))

        # ���f���̕ۑ�
        self.model.save('model.h5')