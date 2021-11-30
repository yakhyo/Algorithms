import numpy as np
import cv2
import os
import random


def is_num_list_or_tuple(objects):
    for obj in objects:
        if not isinstance(obj, int):
            return False
    return True


def verify_image(object):
    if isinstance(object, np.ndarray):
        pass
    elif isinstance(object, list):
        img_list = object
        for img in img_list:
            if not isinstance(img, np.ndarray):
                raise Exception("Expected numpy array or list of numpy arrays")
    else:
        raise Exception("Expected numpy array or list of numpy arrays")


def generate_shadow_coordinates(img_shape, num_shadows, rectangular_roi, shadow_dimension):
    vertices_list = []
    x1 = rectangular_roi[0]
    y1 = rectangular_roi[1]
    x2 = rectangular_roi[2]
    y2 = rectangular_roi[3]
    for index in range(num_shadows):
        vertex = []
        for dimensions in range(shadow_dimension):  # Dimensionality of the shadow polygon
            vertex.append((random.randint(x1, x2), random.randint(y1, y2)))
        vertices = np.array([vertex], dtype=np.int32)  # single shadow vertices
        vertices_list.append(vertices)
    return vertices_list  # List of shadow vertices


def shadow_process(image, num_shadows, x1, y1, x2, y2, shadow_dimension):
    img_hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    mask = np.zeros_like(image)

    img_shape = image.shape
    vertices_list = generate_shadow_coordinates(img_shape, num_shadows, (x1, y1, x2, y2), shadow_dimension)

    for vertices in vertices_list:
        cv2.fillPoly(mask, vertices, 255)

    # if red channel is hot, image's "Lightness" channel's brightness is lowered
    img_hls[:, :, 1][mask[:, :, 0] == 255] = img_hls[:, :, 1][mask[:, :, 0] == 255] * 0.5

    img_rgb = cv2.cvtColor(img_hls, cv2.COLOR_HLS2RGB)
    return img_rgb


def add_shadow(image, num_shadows=1, rect_roi=(-1, -1, -1, -1), shadow_dimension=5):
    # ROI:(top-left x1,y1, bottom-right x2,y2), shadow_dimension=no. of sides of polygon generated
    verify_image(image)
    if not (isinstance(num_shadows, int) and 1 <= num_shadows <= 10):
        raise Exception("Num. of shadows need to be between [1:10]")
    if not (isinstance(shadow_dimension, int) and 3 <= shadow_dimension <= 10):
        raise Exception("Polygon dim. can not be smaller than 3 and greater than 10")
    if isinstance(rect_roi, tuple) and is_num_list_or_tuple(rect_roi) and len(rect_roi) == 4:
        x1 = rect_roi[0]
        y1 = rect_roi[1]
        x2 = rect_roi[2]
        y2 = rect_roi[3]
    else:
        raise Exception("Rectangular ROI dims are not valid")
    if rect_roi == (-1, -1, -1, -1):
        x1 = 0

        if isinstance(image, np.ndarray):
            y1 = image.shape[0] // 2
            x2 = image.shape[1]
            y2 = image.shape[0]
        else:
            y1 = image[0].shape[0] // 2
            x2 = image[0].shape[1]
            y2 = image[0].shape[0]

    elif x1 == -1 or y1 == -1 or x2 == -1 or y2 == -1 or x2 <= x1 or y2 <= y1:
        raise Exception("Invalid rectangular ROI")
    if isinstance(image, list):
        img_rgb = []
        image_list = image
        for img in image_list:
            output = shadow_process(img, num_shadows, x1, y1, x2, y2, shadow_dimension)
            img_rgb.append(output)
    else:
        output = shadow_process(image, num_shadows, x1, y1, x2, y2, shadow_dimension)
        img_rgb = output

    return img_rgb


if __name__ == '__main__':
    root = './dataset'
    for name in os.listdir(root):
        im_path = os.path.join(root, name)
        image = cv2.imread(im_path, cv2.COLOR_BGR2RGB)  # BGR -> RGB
        
        shadowed_image = add_shadow(image)
        stacked_image = np.hstack((image, shadowed_image))  # stacking image and shadowed image
        
        cv2.imshow('display', stacked_image)  # displaying stacked image
        cv2.waitKey(0)

