
# https://theailearner.com/2020/11/03/opencv-minimum-area-rectangle/
# Clarification of angle_of_rot
class Bounding_Box:
    def __init__(self, filepath, rect) -> None:
        self.filepath = filepath
        self.centroid_x = rect[0][0]
        self.centroid_y = rect[0][1]
        self.width = rect[1][0]
        self.height = rect[1][1]
        self.rotation = rect[2]

    def get_dimension_ratio(self):
        return self.height / self.width