from .preprocessing_wizard import PPWizard
import tensorflow as tf
from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator


class Augmentation(PPWizard):
    def __init__(self):
        super().__init__()

    def preprocess(self, dataset):
        data = []
        data_generator = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            fill_mode='nearest'
        )
        for image in dataset:
            img = image.reshape((1,) + image.shape)
            augmented_images = data_generator.flow(img, batch_size=1)
            data.append(augmented_images.__getitem__(0))
        return data
