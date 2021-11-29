import os
import cv2
import json
import numpy as np


def mask_generate(root_path: str, json_path: str, save_folder: str, imshow: bool, imsave: bool) -> None:
    """
    :type root_path: string, path to root folder
    :type json_path: string, path to json file
    """
    with open(json_path, 'r') as js:
        objects = json.load(js)

    for object in objects:

        object = objects[object]
        filename = object['filename']
        size = object['size']
        regions = object['regions']
        path = os.path.join(root_path, filename)
        image = cv2.imread(path, cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape

        for region in regions:
            shape_attributes = region['shape_attributes']
            region_attributes = region['region_attributes']
            car = region_attributes['car']
            name = shape_attributes['name']
            # use only main car images
            if car == 'car-a':
                all_points_x = shape_attributes['all_points_x']
                all_points_y = shape_attributes['all_points_y']

                points = [[x, y] for x, y in zip(all_points_x, all_points_y)]
                points_np = np.array(points)

                # prepare mask
                mask = np.zeros((h, w), dtype='uint8')
                cv2.fillConvexPoly(mask, points_np, 1)

                # finding rectangle coordinates to crop the car area
                x_min, y_min = points_np.min(axis=0)
                x_max, y_max = points_np.max(axis=0)

                # mask overlay image
                masked = cv2.bitwise_and(image, image, mask=mask)
                masked = masked[y_min:y_max, x_min:x_max]

                # save the image
                if imsave:
                    cv2.imwrite(os.path.join(save_folder, filename), masked)

                if imshow:
                    cv2.imshow('masked', masked)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()

            else:
                pass


if __name__ == "__main__":
    root_path = './train'
    json_path = './train/via_region_data.json'
    save_folder = './cropped'
    os.makedirs(save_folder, exist_ok=True)

    mask_generate(root_path=root_path, json_path=json_path, save_folder=save_folder, imshow=True, imsave=False)
