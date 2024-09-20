import os
import time
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

class InferenceModel:
    def __init__(self, model_path):
        """Initialize the model by loading it."""
        self.model = load_model(model_path)
    
    def preprocess_image(self, image_path):
        """Preprocess the image for the model."""
        image = load_img(image_path, color_mode='grayscale', target_size=(784, 2112))
        image_array = img_to_array(image) / 255.0  # Normalize the image
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
        return image_array
    
    def infer(self, image_path):
        # 推論方法あってる？
        """Perform inference on the input image."""
        image = self.preprocess_image(image_path)
        start_time = time.time()
        output = self.model.predict(image)
        end_time = time.time()
        
        # Mean Squared Error as a measure of accuracy
        mse = np.mean((output - image) ** 2)
        inference_time = end_time - start_time
        
        return {
            "accuracy": float(mse),  # Convert to float
            "inference_time": float(inference_time)  # Convert to float
        }

# Example usage:
# model = InferenceModel("./model/some_model.keras")
# result = model.infer("./DamagedImages/sample_image.png")
# print(result)
