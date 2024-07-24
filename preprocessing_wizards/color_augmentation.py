from preprocessing_wizards.preprocessing_wizard import PPWizard
from torchvision import transforms


class ColorAugmentation(PPWizard):
    def __init__(self, brightness, contrast, saturation, hue):
        super().__init__()
        self.color_aug = transforms.ColorJitter(brightness=brightness, contrast=contrast,
                                                           saturation=saturation, hue=hue)

    def preprocess(self, data):
        return [self.color_aug(img) for img in data]
