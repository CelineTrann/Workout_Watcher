import cv2 as cv
import numpy as np

def read_rescale(filepath, scale=0.2):
    img = cv.imread(filepath)
    img = cv.resize(img, (0, 0), fx = scale, fy = scale) 
    img = cv.bitwise_not(img)
    return img

def process_image(img, kernal=(3,3), threshold=0):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.blur(gray, kernal)
    ret, thresh = cv.threshold(blur, threshold, 255, 0)
    return thresh

def connect_objects(img, kernal=(10,10), min_area=1000, min_height=100, min_width=100):
    # Closing of images
    kernel = np.ones(kernal, np.uint8)
    closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

    # Connected Components
    analysis = cv.connectedComponentsWithStats(closing, 4, stats=cv.CV_32S)
    (totalLabels, label_ids, values, centroid) = analysis

    output = np.zeros(img.shape, dtype="uint8")

    # Loop through each component
    for i in range(1, totalLabels):
        area = values[i, cv.CC_STAT_AREA]  
        height = values[i, cv.CC_STAT_HEIGHT]
        width = values[i, cv.CC_STAT_WIDTH]
    
        # If component greater than value add to mask 
        # Used to further filter out noise
        if (area > min_area) and (height > min_height) and (width > min_width):
            componentMask = (label_ids == i).astype("uint8") * 255
            output = cv.bitwise_or(output, componentMask)

    return output, closing

def find_min_bounding_box(analyze_img, view_image):
    contours = cv.findContours(analyze_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    number = 0
    for cntr in contours:
        rect = cv.minAreaRect(cntr)
        box = np.int0(cv.boxPoints(rect))
        cv.drawContours(view_image, [box], 0, (36,255,12), 3) 
        number += 1

    return view_image, number
