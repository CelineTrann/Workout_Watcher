import process as p
import sys
import os

import cv2 as cv
import process_data as pd
from read import read_file, show_img

def main(path, display_img=False, data_label="foot", output="test1.csv"):
    box_data_list = []

    for base_file, data_file in zip(base_files, data_files):
        base_filepath = os.path.join(path, base_file)
        data_filepath = os.path.join(path, data_file)
        img = read_file(base_filepath, data_filepath, threshold=0)

        p_img = p.process_image(img, threshold=40)
        filtered_c_img, c_img = p.connect_objects(p_img, kernal=(3,3), min_area=40, min_height=5, min_width=7)
        bb_img, rects, number = p.find_min_bounding_box(filtered_c_img, img.copy()) 

        if display_img:
            show_img("image", img)
            show_img("p img", p_img)
            show_img("c image", c_img)
            show_img("filtered", filtered_c_img)
            show_img("bb-img", bb_img)

        for rect in rects:
            # Save Data
            box_data = pd.Bounding_Box(data_filepath, rect, data_label)
            box_data_list.append(box_data)

            # Rotate and Crop Image
            crop_img = p.crop_minarearect(img, rect)

            if display_img:
                show_img("crop", crop_img)

        print(f"{data_filepath} - {number} objects")
        
        
    pd.create_data_csv(box_data_list, output)

# ----------------------------------------------------------------------------------------------------------------------------

# Left Foot
base_files = ['baself10.txt', 'baself11.txt', 'baself12.txt', 'baself13.txt', 'baself14.txt', 
              'baself15.txt', 'baself16.txt', 'baself17.txt', 'baself18.txt', 'baself19.txt', 
              'baself1.txt', 'baself20.txt', 'baself21.txt', 'baself22.txt', 'baself23.txt', 
              'baself24.txt', 'baself25.txt', 'baself26.txt', 'baself27.txt', 'baself28.txt', 
              'baself29.txt', 'baself2.txt', 'baself30.txt', 'baself31.txt', 'baself32.txt', 
              'baself33.txt', 'baself34.txt', 'baself35.txt', 'baself36.txt', 'baself3.txt', 
              'baself4.txt', 'baself5.txt', 'baself6.txt', 'baself7.txt', 'baself8.txt', 'baself9.txt']

data_files = ['leftf10_par.txt', 'leftf11_par.txt', 'leftf12_par.txt', 'leftf13_per.txt', 'leftf14_per.txt', 
              'leftf15_per.txt', 'leftf16_per.txt', 'leftf17_per.txt', 'leftf18_per.txt', 'leftf19_per.txt', 
              'leftf1_par.txt', 'leftf20_per.txt', 'leftf21_per.txt', 'leftf22_per.txt', 'leftf23_per.txt', 
              'leftf24_per.txt', 'leftf25_ang.txt', 'leftf26_ang.txt', 'leftf27_ang.txt', 'leftf28_ang.txt', 
              'leftf29_ang.txt', 'leftf2_par.txt', 'leftf30_ang.txt', 'leftf31_ang.txt', 'leftf32_ang.txt', 
              'leftf33_ang.txt', 'leftf34_ang.txt', 'leftf35_ang.txt', 'leftf36_ang.txt', 'leftf3_par.txt', 
              'leftf4_par.txt', 'leftf5_par.txt', 'leftf6_par.txt', 'leftf7_par.txt', 'leftf8_par.txt', 'leftf9_par.txt']

main("Data\Data (02.21)\Left Foot", False, 'foot')

# ----------------------------------------------------------------------------------------------------------------------------

# Right Foot
base_files = ['baserf10.txt', 'baserf11.txt', 'baserf12.txt', 'baserf13.txt', 'baserf14.txt', 
              'baserf15.txt', 'baserf16.txt', 'baserf17.txt', 'baserf18.txt', 'baserf19.txt', 
              'baserf1.txt', 'baserf20.txt', 'baserf21.txt', 'baserf22.txt', 'baserf23.txt', 
              'baserf24.txt', 'baserf25.txt', 'baserf26.txt', 'baserf27.txt', 'baserf28.txt', 
              'baserf29.txt', 'baserf2.txt', 'baserf30.txt', 'baserf31.txt', 'baserf32.txt', 
              'baserf33.txt', 'baserf34.txt', 'baserf35.txt', 'baserf36.txt', 'baserf3.txt', 
              'baserf4.txt', 'baserf5.txt', 'baserf6.txt', 'baserf7.txt', 'baserf8.txt', 'baserf9.txt']

data_files = ['rightf10_par.txt', 'rightf11_par.txt', 'rightf12_par.txt', 'rightf13_per.txt', 'rightf14_per.txt', 
              'rightf15_per.txt', 'rightf16_per.txt', 'rightf17_per.txt', 'rightf18_per.txt', 'rightf19_per.txt', 
              'rightf1_par.txt', 'rightf20_per.txt', 'rightf21_per.txt', 'rightf22_per.txt', 'rightf23_per.txt', 
              'rightf24_per.txt', 'rightf25_ang.txt', 'rightf26_ang.txt', 'rightf27_ang.txt', 'rightf28_ang.txt', 
              'rightf29_ang.txt', 'rightf2_par.txt', 'rightf30_ang.txt', 'rightf31_ang.txt', 'rightf32_ang.txt', 
              'rightf33_ang.txt', 'rightf34_ang.txt', 'rightf35_ang.txt', 'rightf36_ang.txt', 'rightf3_par.txt', 
              'rightf4_par.txt', 'rightf5_par.txt', 'rightf6_par.txt', 'rightf7_par.txt', 'rightf8_par.txt', 'rightf9_par.txt']

main("Data\Data (02.21)\Right Foot", False, 'foot')

# ----------------------------------------------------------------------------------------------------------------------------

# Left Hand
base_files = ['baselh10.txt', 'baselh11.txt', 'baselh12.txt', 'baselh13.txt', 'baselh14.txt', 
              'baselh15.txt', 'baselh16.txt', 'baselh17.txt', 'baselh18.txt', 'baselh19.txt', 
              'baselh1.txt', 'baselh20.txt', 'baselh21.txt', 'baselh22.txt', 'baselh23.txt', 
              'baselh24.txt', 'baselh25.txt', 'baselh26.txt', 'baselh27.txt', 'baselh28.txt', 
              'baselh29.txt', 'baselh2.txt', 'baselh30.txt', 'baselh31.txt', 'baselh32.txt', 
              'baselh33.txt', 'baselh34.txt', 'baselh35.txt', 'baselh36.txt', 'baselh3.txt', 
              'baselh4.txt', 'baselh5.txt', 'baselh6.txt', 'baselh7.txt', 'baselh8.txt', 'baselh9.txt']

data_files = ['lefth10_per.txt', 'lefth11_per.txt', 'lefth12_per.txt', 'lefth13_par.txt', 'lefth14_par.txt', 
              'lefth15_par.txt', 'lefth16_par.txt', 'lefth17_par.txt', 'lefth18_par.txt', 'lefth19_par.txt', 
              'lefth1_per.txt', 'lefth20_par.txt', 'lefth21_par.txt', 'lefth22_par.txt', 'lefth23_par.txt', 
              'lefth24_par.txt', 'lefth25_ang.txt', 'lefth26_ang.txt', 'lefth27_ang.txt', 'lefth28_ang.txt', 
              'lefth29_ang.txt', 'lefth2_per.txt', 'lefth30_ang.txt', 'lefth31_ang.txt', 'lefth32_ang.txt', 
              'lefth33_ang.txt', 'lefth34_ang.txt', 'lefth35_ang.txt', 'lefth36_ang.txt', 'lefth3_per.txt', 
              'lefth4_per.txt', 'lefth5_per.txt', 'lefth6_per.txt', 'lefth7_per.txt', 'lefth8_per.txt', 'lefth9_per.txt']

main("Data\Data (02.21)\Left Hand", False, 'hand')

# ----------------------------------------------------------------------------------------------------------------------------

# Right Hand
base_files = ['base10.txt', 'base11.txt', 'base12.txt', 'base13.txt', 'base14.txt', 
              'base14.txt', 'base15.txt', 'base16.txt', 'base17.txt', 'base18.txt', 
              'base19.txt', 'base1.txt', 'base20.txt', 'base21.txt', 'base22.txt', 
              'base23.txt', 'base24.txt', 'base25.txt', 'base26.txt', 'base27.txt', 
              'base28.txt', 'base29.txt', 'base2.txt', 'base30.txt', 'base31.txt', 
              'base32.txt', 'base33.txt', 'base34.txt', 'base35.txt', 'base36.txt', 
              'base3.txt', 'base4.txt', 'base5.txt', 'base6.txt', 'base7.txt', 
              'base8.txt', 'base9.txt']

data_files = ['righth10_per.txt', 'righth11_per.txt', 'righth12_per.txt', 'righth13_par.txt', 'righth14_par.txt', 
              'righth14_per.txt', 'righth15_par.txt', 'righth16_par.txt', 'righth17_par.txt', 'righth18_par.txt', 
              'righth19_par.txt', 'righth1_per.txt', 'righth20_par.txt', 'righth21_par.txt', 'righth22_par.txt', 
              'righth23_par.txt', 'righth24_par.txt', 'righth25_ang.txt', 'righth26_ang.txt', 'righth27_ang.txt', 
              'righth28_ang.txt', 'righth29_ang.txt', 'righth2_per.txt', 'righth30_ang.txt', 'righth31_ang.txt', 
              'righth32_ang.txt', 'righth33_ang.txt', 'righth34_ang.txt', 'righth35_ang.txt', 'righth36_ang.txt', 
              'righth3_per.txt', 'righth4_per.txt', 'righth5_per.txt', 'righth6_per.txt', 'righth7_per.txt', 
              'righth8_per.txt', 'righth9_per.txt']

main("Data\Data (02.21)\Right Hand", False, 'hand')


