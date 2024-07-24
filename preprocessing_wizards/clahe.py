from .preprocessing_wizard import PPWizard
import cv2

class CLAHE(PPWizard):
    def __init__(self, cliplimit, gridsize):
        super().__init__()
        self.cliplimit = cliplimit
        self.gridsize = gridsize

    def preprocess(self, dataset):
        data = []
        for img in dataset:
            clahe = cv2.createCLAHE(clipLimit=self.cliplimit, tileGridSize=self.gridsize)
            cl1 = clahe.apply(img)
            cl1 = cv2.cvtColor(cl1, cv2.COLOR_GRAY2RGB)
            data.append(cl1)
        return data