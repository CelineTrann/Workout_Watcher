import numpy as np
import cv2 as cv
import os
import sys

def show_img(name, img):
    cv.namedWindow(f"{name}", cv.WINDOW_KEEPRATIO)
    cv.imshow(f"{name}", img)
    cv.resizeWindow(f"{name}", 500, 500)
    cv.waitKey(0)


def convert_to_img(name, base_nparray, data_nparray, img_show=False, threshold=0):
    heatmapshow = None
    nparray = data_nparray - base_nparray
    
    np.set_printoptions(threshold=sys.maxsize)
    print(f'{nparray}')
    
        
    nparray[nparray < threshold] = 0
    
    nparray[4:63, 4:12] = nparray[4:63, 4:12]*2.5
    nparray[4:63, 12:20] = nparray[4:63, 12:20]*2
    row_mean = np.mean(nparray, axis = 1)
    col_mean = np.mean(nparray, axis = 0)  
    row_co = 1/(col_mean+0.000001)
    row_co = 0.5*(row_co - np.min(row_co))/(np.max(row_co)-np.min(row_co))
    print(row_co)
    nparray[nparray < row_mean[:,None]+row_co] = 0
    nparray[nparray < col_mean[None,:]*1.5] = 0
    
    nparray[41:63, 0:28] = nparray[41:63, 0:28]*1.5
    
    heatmapshow = cv.normalize(nparray, heatmapshow, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    heatmapshow = cv.applyColorMap(heatmapshow, cv.COLORMAP_BONE)

    if img_show:
        show_img(name, heatmapshow)

    return heatmapshow

def read_all_file(directory, img_show=False, threshold=40):
    all_files = os.listdir(directory)
    txt_files = [x for x in all_files if x[-4:] == '.txt']
    base_files = [f'{x[:-4]}_{x[-4:]}' for x in txt_files if x[:4] == 'base']
    data_files = [x for x in txt_files if x[:4] != 'base']

    base_files.sort(reverse=False)
    data_files.sort(reverse=False)

    print(base_files)
    print(data_files)

    for base_file, data_file in zip(base_files, data_files):
        base_filename = f'{base_file[:-5]}{base_file[-4:]}'
        base = np.genfromtxt(f"{directory}\{base_filename}", delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))
        data = np.genfromtxt(f"{directory}\{data_file}", delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))
        
        subtract = data - base
        img = convert_to_img(f'{data_file} - {base_filename}', subtract, img_show, threshold)


def read_file(base, file, img_show=False, threshold=0):
    base_data = np.genfromtxt(base, delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))
    data = np.genfromtxt(file, delimiter=",", encoding='UTF-8', unpack=False, usecols=range(24))

    img = convert_to_img("subtract", base_data, data, img_show, threshold)
    return img


if __name__ == '__main__':
    # read_file("Python Plotting\\base3.txt", "Python Plotting\\hand3.txt")
    #read_all_file("Data\Data (02.21)\Right Hand", img_show=True)
    m = np.mean([ 0.3577203,   0.46406958,  0.58330968,  0.5962005,   0.54463722,  0.57041886,
   0.52530098,  0.52207828,  0.57686427,  0.61553674,  0.62842756,  0.61231403,
   0.61553674,  0.60264591,  0.58653239,  0.58653239,  0.5962005,   0.63809567,
   0.72510872,  0.81534447,  0.91524834,  0.87979858,  0.82823529,  0.70254978,
   0.16113527,  0, 0, 0])
    print(m)