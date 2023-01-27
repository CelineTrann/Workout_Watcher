# Workout_Watcher

## Image Processing
This is the process of cleaning up our data and processing it to acquire data from it

In the `process.py` folder are helper functions that are steps in the image processing process.

`read_rescale(filepath, scale=0.2)`
* takes in a file path and reads the image
* the image is rescaled to fit on the screen
* the colours of the image are inverted as they currently have a white background (*will change)

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

### How to Run
1. Clone the project
2. Open the project
3. Use the terminal command

    ``` bash
        python ImageProcessing\main.py <path_to_image_folder>
    ```

    For example,
    ```
    python ImageProcessing\main.py Images\Left_foot
    ```