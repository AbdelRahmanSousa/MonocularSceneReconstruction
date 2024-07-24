from .preprocessing_wizard import PPWizard
import cv2


class Resizing(PPWizard):
    def __init__(self, high=700, low=500):
        super().__init__()
        self.high = high
        self.low = low

    def preprocess(self, dataset):
        data = []
        for img in dataset:
            if img.shape[0] > img.shape[1]:
                data.append(cv2.resize(img, (self.low, self.high)))
            elif img.shape[1] > img.shape[0]:
                data.append(cv2.resize(img, (self.high, self.low)))
            else:
                data.append((cv2.resize(img, (self.high, self.high))))
        return data
