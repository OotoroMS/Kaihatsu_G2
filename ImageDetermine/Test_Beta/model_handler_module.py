import tensorflow as tf
import os
import numpy as np

class ModelHandler:
    def __init__(self, input_shape, model_save_path='./saved_model'):
        """
        :param input_shape: モデルの入力サイズ (height, width, channels)
        :param model_save_path: モデルの保存先パス
        """
        self.input_shape = input_shape
        self.model_save_path = model_save_path
        self.model = None  # モデルを初期化するが、トレーニング時にのみ構築する

    def _build_autoencoder(self):
        """
        AutoEncoderモデルを構築する
        :return: 構築されたAutoEncoderモデル
        """
        input_layer = tf.keras.layers.Input(shape=self.input_shape)
    
        # Encoder
        x = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')(input_layer)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D((2, 2), padding='same')(x)  # サイズが1/2に
        x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D((2, 2), padding='same')(x)  # サイズが1/4に
        x = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D((2, 2), padding='same')(x)  # サイズが1/8に
        x = tf.keras.layers.Conv2D(512, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        encoded = tf.keras.layers.MaxPooling2D((2, 2), padding='same')(x)  # サイズが1/16に
    
        # Decoder
        x = tf.keras.layers.Conv2D(512, (3, 3), activation='relu', padding='same')(encoded)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.UpSampling2D((2, 2))(x)  # サイズが1/8に戻る
        x = tf.keras.layers.Conv2D(256, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.UpSampling2D((2, 2))(x)  # サイズが1/4に戻る
        x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.UpSampling2D((2, 2))(x)  # サイズが1/2に戻る
        x = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.UpSampling2D((2, 2))(x)  # 元のサイズに戻る
    
        decoded = tf.keras.layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)  # 元の入力サイズと一致する出力
        model = tf.keras.models.Model(input_layer, decoded)
        model.compile(optimizer='adam', loss='mse')
        return model

    def train_model(self, train_data, epochs=50, batch_size=32):
        """
        モデルをトレーニングする
        :param train_data: トレーニングデータ（NumPy配列）
        :param epochs: エポック数
        :param batch_size: バッチサイズ
        """
        # モデルの構築をトレーニング時にのみ行う
        self.model = self._build_autoencoder()
        # トレーニングデータを用いてAutoEncoderをトレーニング
        self.model.fit(train_data, train_data, epochs=epochs, batch_size=batch_size, validation_split=0.2)
        # トレーニング後にモデルを保存
        self.save_model()

    def save_model(self, model_save_path=None):
        """
        モデルを保存する
        :param model_save_path: モデルの保存先パス（オプション）
        """
        if model_save_path is not None:
            self.model_save_path = model_save_path
        if not os.path.exists(self.model_save_path):
            os.makedirs(self.model_save_path)
        self.model.save(self.model_save_path)
        print(f"Model saved to {self.model_save_path}")

    def load_model(self, model_save_path=None):
        """
        保存されたモデルを読み込む
        :param model_save_path: 読み込むモデルのパス（オプション）
        """
        if model_save_path is not None:
            self.model_save_path = model_save_path
        if os.path.exists(self.model_save_path):
            self.model = tf.keras.models.load_model(self.model_save_path)
            print(f"Model loaded from {self.model_save_path}")
        else:
            raise FileNotFoundError(f"No saved model found at path: {self.model_save_path}")

    def predict(self, input_image):
        """
        入力画像に対して推論を行う
        :param input_image: 入力画像（NumPy配列）
        :return: 推論結果（再構成された画像）
        """
        input_image = np.expand_dims(input_image, axis=0)  # バッチ次元を追加
        reconstructed_image = self.model.predict(input_image)
        return np.squeeze(reconstructed_image, axis=0)  # バッチ次元を削除

if __name__ == "__main__":
    # モデルモジュールの例
    model_handler = ModelHandler(input_shape=(128, 128, 3))
    
    # サンプルデータを用意（ここではランダムデータを使用）
    sample_train_data = np.random.rand(100, 128, 128, 3)
    
    # モデルのトレーニング
    model_handler.train_model(train_data=sample_train_data, epochs=10)
    
    # モデルの読み込みと推論の例
    model_handler.load_model()
    sample_input_image = np.random.rand(128, 128, 3)
    reconstructed_image = model_handler.predict(sample_input_image)
    print("Prediction completed.")