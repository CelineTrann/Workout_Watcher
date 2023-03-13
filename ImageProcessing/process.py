import cv2 as cv
import numpy as np

def process_image(img, kernal=(3,3), threshold=0):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.blur(gray, kernal)
    ret, thresh = cv.threshold(blur, threshold, 255, 0)
    return gray

def connect_objects(img, kernal=(10,10), min_area=40, min_height=6, min_width=6):
    # Closing of images
    kernel = np.ones(kernal, np.uint8)
    #closing = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
    
    # threshold and blur
    ret, closing = cv.threshold(img, 70, 255, 0)
    closing = cv.blur(closing, (3, 3))
    
    # Connected Components
    analysis = cv.connectedComponentsWithStats(closing, 4, stats=cv.CV_32S)
    (totalLabels, label_ids, values, centroid) = analysis

    output = np.zeros(img.shape, dtype="uint8")

    # Loop through each component
    for i in range(1, totalLabels):
        area = values[i, cv.CC_STAT_AREA]  
        height = values[i, cv.CC_STAT_HEIGHT]
        width = values[i, cv.CC_STAT_WIDTH]

        # print(f"A: {area}, H: {height}, W: {width}")
    
        # If component greater than value add to mask 
        # Used to further filter out noise
        if (area >= min_area) or ((height >= min_height) and (width >= min_width)):
            componentMask = (label_ids == i).astype("uint8") * 255
            output = cv.bitwise_or(output, componentMask)

    return output, closing

def find_min_bounding_box(analyze_img, view_image):
    contours = cv.findContours(analyze_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    number = 0
    rects = []
    for cntr in contours:
        rect = cv.minAreaRect(cntr)
        box = np.int0(cv.boxPoints(rect))
        cv.drawContours(view_image, [box], 0, (36,255,12), 1) 
        
        number += 1
        rects.append(rect)


    return view_image, rects, number


def crop_minarearect(img, rect):
    # Create mask for Bounding Box
    mask = np.zeros_like(img)

    # draw the rotated bounding box on the mask
    box = np.int0(cv.boxPoints(rect))
    points = np.int0(box)
    cv.fillPoly(mask, [points], color=(255, 255, 255))

    # apply the mask to the input image to crop it
    cropped_img = cv.bitwise_and(img.copy(), mask)

    # Get center, size, and angle from rect
    center, size, angle = rect
    size  = tuple(x+3 for x in size)
    size = (size[1], size[0])

    # Convert to int W
    center, size = tuple(map(int, center)), tuple(map(int, size))
    
    if angle % 90 != 0:
        # Get rotation matrix for rectangle
        M = cv.getRotationMatrix2D( center, angle, 1)
        
        # Perform rotation on src image
        dst = cv.warpAffine(cropped_img, M, cropped_img.shape[:2])
        out = cv.getRectSubPix(dst, size, center)
    else:
        out = cv.getRectSubPix(cropped_img, size, center)

    return out, points

def get_sections_mean(img):
    rows, cols = img.shape[0], img.shape[1]
    row_mid, col_mid = int(rows/2), int(cols/2)

    Ltop = img[0:row_mid, 0:col_mid]
    Rtop = img[0:row_mid, col_mid:cols]
    Lbottom = img[row_mid:rows, 0:col_mid]
    Rbottom = img[row_mid:rows, col_mid:cols]
    
    return [Ltop.mean(), Rtop.mean(), Lbottom.mean(), Rbottom.mean()]

# For Debugging, see process_data.py
def get_data_from_box(rect):
    center_x, center_y = rect[0]
    box_width, box_height = rect[1]
    angle_of_rot = rect[2]

    print(f"centeroid: {center_x}, {center_y}")
    print(f"box dimensions: {box_width} x {box_height}")
    print(f"Angle of rotation: {angle_of_rot} degrees")


# Used for debugging
# if __name__ == "__main__":
#     img = read_rescale("Images\Left_foot\\1-4.jpeg")
#     p_img = process_image(img, threshold=10)
#     filtered_c_img, c_img = connect_objects(p_img)
#     bb_img, rect, number = find_min_bounding_box(filtered_c_img, c_img)

#     result = get_sections_mean(p_img)
#     print(result)