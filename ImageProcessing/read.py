import numpy as np
import cv2 as cv
import os

def show_img(name, img):
    cv.namedWindow(f"{name}", cv.WINDOW_KEEPRATIO)
    cv.imshow(f"{name}", img)
    cv.resizeWindow(f"{name}", 500, 500)
    cv.waitKey(0)


def convert_to_img(name, nparray, img_show=False, threshold=0):
    heatmapshow = None
    nparray[nparray < threshold] = 0
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

    subtract = data - base_data
    img = convert_to_img("subtract", subtract, img_show, threshold)
    return img


if __name__ == '__main__':
    # read_file("Python Plotting\\base3.txt", "Python Plotting\\hand3.txt")
    read_all_file("Data\Data (02.21)\Right Hand", img_show=True)