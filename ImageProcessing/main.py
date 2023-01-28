import process as p
import sys
import os

import cv2 as cv

def main(path):
    dir_list = os.listdir(path)

    for file in dir_list:
        filepath = os.path.join(path, file)
        img = p.read_rescale(filepath)
        p_img = p.process_image(img, threshold=10)
        filtered_c_img, c_img = p.connect_objects(p_img)
        bb_img, number = p.find_min_bounding_box(filtered_c_img, img)

        cv.imshow(filepath, bb_img)
        cv.waitKey(0)
        print(f"{filepath} - {number} objects")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(f"Usage: {sys.argv[0]} <directory_to_images>")

    path = sys.argv[1]
    main(path)
