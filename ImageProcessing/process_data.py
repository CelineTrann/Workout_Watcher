import csv

# https://theailearner.com/2020/11/03/opencv-minimum-area-rectangle/
# Clarification of angle_of_rot
class Bounding_Box:
    def __init__(self, filepath, rect, label) -> None:
        self.filepath = filepath
        self.centroid_x = rect[0][0]
        self.centroid_y = rect[0][1]
        self.width = rect[1][0]
        self.height = rect[1][1]
        self.rotation = rect[2]
        self.label = label

    def set_label(self, label) -> None:
        self.label = label

    def get_dimension_ratio(self):
        return self.height / self.width
    
def create_data_csv(data_list: list[Bounding_Box], filename):
    try: 
        with open(filename, "a", newline='') as f:
            writer = csv.writer(f)
            for d in data_list:
                writer.writerow([d.centroid_x, d.centroid_y, d.height, d.width, d.rotation, d.label])
    except BaseException as e:
        print("BaseException: ", filename)
    else:
        print("Data has been loaded successfully!")