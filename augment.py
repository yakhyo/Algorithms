import cv2
import torch
import torchvision
import torchvision.transforms.functional as TF


class AdjustBrightness:
    def __init__(self):
        pass

    def __call__(self, image, brightness_factor=0.2):
        return TF.adjust_brightness(image, brightness_factor)


class AdjustContrast:
    def __init__(self):
        pass

    def __call__(self, image, contrast_factor=0.2):
        return TF.adjust_contrast(image, contrast_factor)


class AdjustGamma:
    def __init__(self):
        pass

    def __call__(self, image, gamma, gain=1):
        return TF.adjust_gamma(image, gamma, gain)


class Rotate90:
    def __init__(self):
        pass

    def rot90_apply(self, image):
        return torch.rot90(image, 0, (2, 3))

    def rot90_back(self, image):
        return torch.rot90(image, 3, (2, 3))


if __name__ == '__main__':
    rotate = Rotate90()

    image = cv2.imread('test.jpg', cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (image.shape[1] // 3, image.shape[0] // 3))
    tensor = torch.from_numpy(image).permute(2, 1, 0).unsqueeze(0)

    image = rotate.rot90_apply(tensor)
    image_1 = image.squeeze().permute(1, 2, 0).numpy()

    image = rotate.rot90_back(image)
    image_2 = image.squeeze().permute(1, 2, 0).numpy()

    cv2.imshow('apply', image_1)
    cv2.imshow('back', image_2)
    cv2.waitKey(0)
