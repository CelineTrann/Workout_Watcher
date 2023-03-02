# Image Processing

## Process
This is the process of cleaning up our data and processing it to acquire data from it

In the `process.py` folder are helper functions that are steps in the image processing process.

`process_image(img, kernal=(3,3), threshold=0)`
* basic image processing 
* converts the image to greyscale
* blurs the image

`connect_objects(img, kernal=(10,10), min_area=1000, min_height=100, min_width=100)`
* performs a closing function on the image to connect close components together
* further filters out the connected objects based on the min_area, min_height, and min_width
* returns an image of the filter componets, and the closed objects

`find_min_bounding_box(analyze_img, view_image)`
* finds the minimum bounding box (smallest rectangle around objects)
* finds the bounding box based on the analyze_img
* draws the bounding box on the view_image
* returns the drawn on image

`crop_minarearect(img, rect)`
* rotates and crops image based on the rotated bounding box around an object
* used to isolate various objects on the mat

`get_sections_mean(img)`
* divided image into quadrant
* returns the mean value of each sections (float)

## Process Data
This is, to my knowledge, how the dimensions and means are situated. The height and width might be swapped though...
![Dimensions](ImageProcessing\dimensions.png)

This is how the rotation of the Bounding Box works
![Bounding Box Rotation](ImageProcessing\rotations.png)

Note that the rotation is calculated from the lowest point of the box with the x-axis

`BoundingBox`
* object containing information about an object
* see files `process_data.py` for what is stored

`Boxes`
* list of bounding boxes

`create_data_csv(data_list: list[Bounding_Box], filename)`
* create csv of Bounding Box data
* used to train ML model