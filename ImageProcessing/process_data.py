import csv
import numpy as np
from enum import Enum

class pressure(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class limb(Enum):
    HAND = 'hand'
    FOOT = 'foot'

class side(Enum):
    RIGHT = 1
    LEFT = 2

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
        self.label: limb = label

    def set_filepath(self, filepath) -> None:
        self.filepath = filepath

    def set_side(self, side_val) -> None:
        self.side = side_val

    def map_pressure(self, pressure_val) -> str:
        if pressure_val > 10:
            return pressure.HIGH
        elif pressure_val < 5:
            return pressure.LOW
        else:
            return pressure.MEDIUM

    def set_mean(self, means: list) -> None:
        self.ltop_mean = self.map_pressure(means[0])
        self.rtop_mean = self.map_pressure(means[1])
        self.lbottom_mean = self.map_pressure(means[2])
        self.rbottom_mean = self.map_pressure(means[3])

    def get_hw_ratio(self):
        return self.height / self.width
    
class Boxes:
    def __init__(self) -> None:
        self.feet: list[Bounding_Box] = []
        self.hands: list[Bounding_Box] = []

    def add_box(self, box: Bounding_Box) -> None:
        if box.label == limb.FOOT:
            self.feet.append(box)
        else:
            self.hands.append(box)

    def is_valid(self) -> bool:
        if len(self.feet) > 2 or len(self.hands) > 2:
            return False
        
        return True
    
    def get_distance(self):
        pass

    def set_side(self, obj: str) -> None:
        if obj == limb.FOOT:
            foot1 = self.feet[0]
            foot2 = self.feet[1]
            
            if foot1.centroid_x > foot2.centroid_x:
                foot1.set_side(side.RIGHT)
                foot2.set_side(side.LEFT)
            else:
                foot1.set_side(side.LEFT)
                foot2.set_side(side.RIGHT)

        else: 
            hand1 = self.hands[0]
            hand2 = self.hands[1]
            
            if hand1.centroid_x > hand2.centroid_x:
                hand1.set_side(side.RIGHT)
                hand2.set_side(side.LEFT)
            else:
                hand1.set_side(side.LEFT)
                hand2.set_side(side.RIGHT)

    def set_side_vertical(self, obj: str):
        pass

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