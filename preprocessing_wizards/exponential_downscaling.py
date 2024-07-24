from preprocessing_wizards.preprocessing_wizard import PPWizard
from torchvision import transforms
from PIL import Image


class ExponentialDownScaling(PPWizard):

    def __init__(self, width, height, num_scales=4, interpolation: transforms.InterpolationMode = Image.ANTIALIAS):
        super().__init__()
        self.num_scales = num_scales
        self.resize = []
        for i in range(self.num_scales):
            s = 2 ** i
            self.resize.append(transforms.Compose([transforms.ToPILImage(), transforms.Resize((width // s, height // s), interpolation=interpolation),transforms.ToTensor()]))

    def preprocess(self, data):
        output = []
        for item in data:
            for i in range(len(self.resize)):
                output.append(self.resize[i](item))
        return output
