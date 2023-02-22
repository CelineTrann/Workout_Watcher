import numpy as np
import cv2 as cv
import os

def show_img(name, img):
    cv.namedWindow(f"{name}", cv.WINDOW_KEEPRATIO)
    cv.imshow(f"{name}", img)
    cv.resizeWindow(f"{name}", 500, 500)
    cv.waitKey(0)


def convert_to_img(name, nparray, show_img=False, threshold=40):
    heatmapshow = None
    nparray[nparray < threshold] = 0
    heatmapshow = cv.normalize(nparray, heatmapshow, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
    heatmapshow = cv.applyColorMap(heatmapshow, cv.COLORMAP_BONE)

    if show_img:
        show_img(name, heatmapshow)

    return heatmapshow

def read_all_file():
    all_files = os.listdir("Python Plotting")
    txt_files = [x for x in all_files if x[-4:] == '.txt']

    for file in txt_files:
        data = np.genfromtxt("Python Plotting\\" + file, delimiter=",", dtype=np.int16)
        img = convert_to_img(file, data)


def read_file(base, file, show_img=False, threshold=40):
    base_data = np.genfromtxt(base, delimiter=",", dtype=np.int16)
    data = np.genfromtxt(file, delimiter=",", dtype=np.int16)

    subtract = data - base_data
    img = convert_to_img("subtract", subtract, show_img, threshold)
    return img

read_file("Python Plotting\\base3.txt", "Python Plotting\\hand3.txt")