import process as p
import sys
import os

import cv2 as cv
import process_data as pd
from read import read_file, show_img

base_files = ["base.txt", "base2.txt", "base3.txt", "base4.txt", "base5.txt", 
            "base6.txt", "base7.txt", "base8.txt", "base9.txt", "base10.txt",
            "basef.txt", "basef2.txt", "basef3.txt", "basef4.txt", "basef5.txt", 
            "basef6.txt", "basef7.txt", "basef8.txt", "basef9.txt", "basef10.txt"]

data_files = ["hand.txt", "hand2.txt", "hand3.txt", "hand4.txt", "hand5.txt", 
              "hand6.txt", "hand7.txt", "hand8.txt", "hand9.txt", "hand10.txt", 
              "foot.txt", "foot2.txt", "foot3.txt", "foot4.txt", "foot5.txt",
              "foot6.txt", "foot7.txt", "foot8.txt", "foot9.txt", "foot10.txt"]

def main(path, display_img=False):
    box_data_list = []

    for base_file, data_file in zip(base_files, data_files):
        base_filepath = os.path.join(path, base_file)
        data_filepath = os.path.join(path, data_file)
        img = read_file(base_filepath, data_filepath, threshold=0)

        p_img = p.process_image(img, threshold=40)
        filtered_c_img, c_img = p.connect_objects(p_img, kernal=(3,3))
        bb_img, rects, number = p.find_min_bounding_box(filtered_c_img, img.copy())

        if display_img:
            show_img("image", img)
            show_img("p img", p_img)
            show_img("c image", c_img)
            show_img("filtered", filtered_c_img)
            show_img("bb-img", bb_img)

        for rect in rects:
            # Save Data
            box_data = pd.Bounding_Box(data_filepath, rect)
            box_data_list.append(box_data)

            # Rotate and Crop Image
            crop_img = p.crop_minarearect(img, rect)

            if display_img:
                show_img("crop", crop_img)

        print(f"{data_filepath} - {number} objects")
        
        
    pd.create_data_csv(box_data_list, "test.csv")


main("Python Plotting", True)

# # python ImageProcessing/main.py "Python Plotting"
# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         raise SystemExit(f"Usage: {sys.argv[0]} <directory_to_images>")

#     path = sys.argv[1]
#     main(path)

