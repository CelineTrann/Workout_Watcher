import ImageProcessing.process as ip
import ImageProcessing.process_data as ipd
import ImageProcessing.read as ir

import numpy as np
import pandas as pd
import pickle

def process_img(base, data, filepath):
    # Load modelfrom file
    with open(filepath, 'rb') as file:
        model = pickle.load(file)

    # process data as image
    img = ir.convert_to_img("curr", base, data, threshold=0)
    p_img = ip.process_image(img, threshold=40)
    filtered_c_img, c_img = ip.connect_objects(p_img, kernal=(3,3), min_area=40, min_height=5, min_width=7)
    bb_img, rects, number = ip.find_min_bounding_box(filtered_c_img, img.copy()) 

    boxes = ipd.Boxes()
    for rect in rects:
        # Save Data
        box_data = ipd.Bounding_Box(rect)

        label = detect_object(model, box_data)
        box_data.set_label(label)

        # Rotate and Crop Image
        crop_img = ip.crop_minarearect(img, rect)
        section_mean = ip.get_sections_mean(crop_img)
        box_data.set_mean(section_mean)

        boxes.add_box(box_data)
        
    return boxes

def detect_object(model, object: ipd.Bounding_Box):  
    x = pd.DataFrame({' height': [object.height], ' width': [object.width]})
    result = model.predict(x)
    print(result)
     
# Debugging
if __name__ == '__main__':
    base_data = np.genfromtxt("Data\Data (02.21)\Left Foot\\baself1.txt", delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))
    data = np.genfromtxt("Data\Data (02.21)\Left Foot\leftf1_par.txt", delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))
    result = process_img(base_data, data, "C:\\Users\\crona\\Downloads\\4B_tron\\Capstone\\Workout_Watcher\\Model\\or_kneighbour.pkl")