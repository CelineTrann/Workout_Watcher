import csv

# https://theailearner.com/2020/11/03/opencv-minimum-area-rectangle/
# Clarification of angle_of_rot
class Bounding_Box:
    def __init__(self, rect) -> None:
        self.centroid_x = rect[0][0]
        self.centroid_y = rect[0][1]
        self.width = rect[1][0]
        self.height = rect[1][1]
        self.rotation = rect[2]

    def set_label(self, label) -> None:
        self.label = label

    def set_filepath(self, filepath) -> None:
        self.filepath = filepath

    def set_mean(self, means: list) -> None:
        self.ltop_mean = means[0]
        self.rtop_mean = means[1]
        self.lbottom_mean = means[2]
        self.rbottom_mean = means[3]

    def get_hw_ratio(self):
        return self.height / self.width
    
class Boxes:
    def __init__(self) -> None:
        self.boxes: list[Bounding_Box] = []

    def add_box(self, box: Bounding_Box) -> None:
        self.boxes.append(box)

    def get_box(self, index: int):
        return self.boxes[index]

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