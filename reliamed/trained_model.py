import os
import io
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

# Load the trained model
model_path = '/workspaces/appDevProj/reliamed/saved_ml_model/med-vit.keras'
model = load_model(model_path)
CATEGORIES = ['Alaxan', 'Bactidol', 'Bioflu', 'Biogesic', 'DayZinc', 'Decolgen', 'Fish Oil', 'Kremil S', 'Medicol', 'Neozep']

from PIL import Image

def display_uploaded_image(imagefile):
    # Open the image file
    image = Image.open(imagefile)
    # Return the image path
    return imagefile.filename

def save_image(imagefile, save_dir="/workspaces/appDevProj/reliamed/static/img"):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    image_path = os.path.join(save_dir, imagefile.filename)
    imagefile.save(image_path)
    return image_path

def preprocess_image(image_path):
    datagen = ImageDataGenerator(preprocessing_function=tf.keras.applications.mobilenet_v2.preprocess_input)
    image = load_img(image_path, target_size=(224, 224), color_mode='rgb')  # Adjust target_size as needed
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    image_array = datagen.flow(image_array, batch_size=1)[0]
    return image_array

def predict_image_class(image_path):
    preprocessed_image = preprocess_image(image_path)
    predictions = model.predict(preprocessed_image)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence_score = predictions[0][predicted_class]

    # # Remove the image after prediction
    # os.remove(image_path)
    
    return CATEGORIES[predicted_class], confidence_score