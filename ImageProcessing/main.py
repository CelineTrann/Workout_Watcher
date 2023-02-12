import process as p
import sys
import os

import cv2 as cv
import process_data as pd
import csv

def create_data_csv(data_list: list[pd.Bounding_Box], filename):
    try: 
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            for d in data_list:
                writer.writerow([d.centroid_x, d.centroid_y, d.height, d.width, d.rotation, d.filepath])
    except BaseException as e:
        print("BaseException: ", filename)
    else:
        print("Data has been loaded successfully!")

def main(path):
    dir_list = os.listdir(path)
    box_data_list = []

    for file in dir_list:
        filepath = os.path.join(path, file)
        img = p.read_rescale(filepath)
        # cv.imshow("image", img)

        p_img = p.process_image(img, threshold=10)
        # cv.imshow("p img", p_img)
        filtered_c_img, c_img = p.connect_objects(p_img)
        # cv.imshow("c image", c_img)
        # cv.imshow("filtered", filtered_c_img)
        bb_img, rects, number = p.find_min_bounding_box(filtered_c_img, img)
        # cv.imshow("bb-img", bb_img)

        for rect in rects:
            # Save Data
            box_data = pd.Bounding_Box(filepath, rect)
            box_data_list.append(box_data)

            # Rotate and Crop Image
            crop_img = p.crop_minarearect(img, rect)
            cv.imshow(f"{filepath}", crop_img)

        print(f"{filepath} - {number} objects")
        
        cv.waitKey(0)
        
    create_data_csv(box_data_list, "test.csv")

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     raise SystemExit(f"Usage: {sys.argv[0]} <directory_to_images>")

    # path = sys.argv[1]
    path = "Images\Left_foot" 
    main(path)

