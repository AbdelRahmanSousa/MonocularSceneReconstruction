from .preprocessing_wizard import PPWizard
from skimage.util import img_as_ubyte
import numpy as np


class WhiteBalancing(PPWizard):
    def __init__(self, percentile=100):
        self.percentile = percentile

    def preprocess(self, dataset):
        data = []
        for image in dataset:
            white_patch_image = img_as_ubyte((image * 1.0 /
                                                  np.percentile(image, self.percentile,
                                                                axis=(0, 1))).clip(0, 1))
            data.append(white_patch_image)
        return data
