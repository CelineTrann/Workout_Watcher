import ImageProcessing.process as ip
import ImageProcessing.process_data as ipd
import ImageProcessing.read as ir

import numpy as np
import pandas as pd
import pickle

def process_img(base, data) -> ipd.Boxes:
    # process data as image
    img, data_copy = ir.convert_to_img("curr", base, data, threshold=0)
    p_img = ip.process_image(img, threshold=40)
    filtered_c_img, c_img = ip.connect_objects(p_img, kernal=(1,1))
    bb_img, rects, number = ip.find_min_bounding_box(filtered_c_img, img.copy()) 
    
    #ir.show_img("img", img)
    #ir.show_img("c-img", c_img)
    #ir.show_img("cFilter-img", filtered_c_img)
    ir.show_img("bb-img", bb_img)
    print(f"Number of objects {number}")
    
    boxes = ipd.Boxes()
    for rect in rects:
        # Save Data
        box_data = ipd.Bounding_Box(rect)
        
        # Get the pressure of each region
        crop_img, points = ip.crop_minarearect(img, rect)
        #ir.show_img("crop", crop_img)
        
        # TODO: For Murphy!
        if box_data.rotation == 90:
            print("Double checking angle...")
            point1 = points[0]
            point2 = points[1]
            point3 = points[2]
            
            print("Position of bounding box: %s %s %s %s"%(point1[1], point3[1]+1, point1[0], point2[0]+1))
            crop_data = data_copy[point1[1]:point3[1]+1, point1[0]:point2[0]+1]
            hei = np.shape(crop_data)[0]
            wid = np.shape(crop_data)[1]
            
            tl = np.mean(crop_data[0:2, 0:2])
            #print("tl: %s"%tl)
            tr = np.mean(crop_data[0:2, (wid-2):(wid+1)])
            #print("tr: %s"%tr)
            bl = np.mean(crop_data[(hei-2):(hei+1), 0:2])
            #print(crop_data[(hei-2):(hei+1), 0:2])
            #print("bl: %s"%bl)
            br = np.mean(crop_data[hei-2:hei+1, wid-2:wid+1])
            #print(crop_data[hei-2:hei+1, wid-2:wid+1])
            #print("br: %s"%br) 
            uTop = np.mean(crop_data[0:2, 0:wid])
            #print(uTop)
            uBottom = np.mean(crop_data[hei-2:hei+1, 0:wid])
            #print(uBottom)
            uCrop = np.mean(crop_data)
            #print("mean of all: %s"%uCrop)
            
#             if tl < uTop * 0.7 and br < uBottom * 0.7:
#                 box_data.rotation = 45
#                 print("Angle corrected to 45.")
#             elif tr < uTop * 0.7 and bl < uBottom * 0.7:
#                 box_data.rotation = 135
#                 print("Angle corrected to 135.")
#             else:
#                 print("No angle correction is required.")
            
            if tl < uCrop * 0.3 and br < uCrop * 0.3:
                # box_data.rotation = 135
                print("Angle corrected to 45.")
            elif tr < uCrop * 0.3 and bl < uCrop * 0.3:
                # box_data.rotation = 225
                print("Angle corrected to 135.")
            else:
                print("No angle correction is required.")
        
        section_mean = ip.get_sections_mean(crop_img)
        box_data.set_mean(section_mean)

        boxes.add_box(box_data)
        
    return boxes
     
# Debugging
if __name__ == '__main__':
    base_data = np.genfromtxt("Data\Data (02.21)\Left Foot\\baself1.txt", delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))
    data = np.genfromtxt("Data\Data (02.21)\Left Foot\leftf1_par.txt", delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))
    
    # Load model from file
    with open("C:\\Users\\crona\\Downloads\\4B_tron\\Capstone\\Workout_Watcher\\Model\\or_kneighbour.pkl", 'rb') as file:
        model = pickle.load(file)
        
    result = process_img(base_data, data, model)