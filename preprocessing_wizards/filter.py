from .preprocessing_wizard import PPWizard
import cv2


class Filtering(PPWizard):
    def __init__(self, D=9, color=75, space=75):
        super().__init__()
        self.D = D
        self.color = color
        self.space = space

    def preprocess(self, dataset):
        data = []
        for img in dataset:
            filteredImage = cv2.bilateralFilter(img, d=self.D, sigmaColor=self.color, sigmaSpace=self.space)
            data.append(filteredImage)
        return data
