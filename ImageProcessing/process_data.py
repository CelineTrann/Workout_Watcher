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

    def get_plural_hand(self):
        return 'hands'
    
    def get_plural_foot(self):
        return 'feet'

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
    
    def get_rotation(self):
        ratio = self.get_hw_ratio()
        if ratio > 1 and self.rotation == 90:
            return self.rotation - 90
        elif ratio < 1 and self.rotation != 90:
            return self.rotation + 90
        
        return self.rotation
    
class Boxes:
    def __init__(self) -> None:
        self.feet: list[Bounding_Box] = []
        self.hands: list[Bounding_Box] = []

    def add_box(self, box: Bounding_Box) -> None:
        if box.label == limb.FOOT.value:
            self.feet.append(box)
        else:
            self.hands.append(box)

    def is_valid(self) -> bool:
        if len(self.feet) > 2 or len(self.hands) > 2:
            return False
        
        return True
    
    def get_obj(self, obj: limb) -> tuple[Bounding_Box, Bounding_Box]:
        if obj == limb.FOOT:
            obj1 = self.feet[0]
            obj2 = self.feet[1]
        else:
            obj1 = self.hands[0]
            obj2 = self.hands[1]

        return obj1, obj2

    def set_side(self, obj: limb) -> None:
        obj1, obj2 = self.get_obj(obj)
            
        if obj1.centroid_x > obj2.centroid_x:
            obj1.set_side(side.RIGHT)
            obj2.set_side(side.LEFT)
        else:
            obj1.set_side(side.LEFT)
            obj2.set_side(side.RIGHT)

    def set_side_vertical(self, obj: limb, bottom_side: side, top_side: side) -> None:
        obj1, obj2 = self.get_obj(obj)

        if obj1.centroid_y < obj2.centroid_y:
            obj1.set_side(bottom_side)
            obj2.set_side(top_side)
        else:
            obj1.set_side(top_side)
            obj2.set_side(bottom_side)

    def get_sides(self, obj: limb) -> tuple[Bounding_Box, Bounding_Box]:
        obj1, obj2 = self.get_obj(obj)

        if obj1.side == side.LEFT:
            left, right = obj1, obj2
        elif obj1.side ==side.RIGHT:
            right, left = obj1, obj2

        return left, right

    def get_distance(self, obj: limb) -> float:
        obj1, obj2 = self.get_obj(obj)
        distance_x = abs(obj1.centroid_x - obj2.centroid_x)
        distance_y = abs(obj1.centroid_y - obj2.centroid_y)
        return distance_x, distance_y
    
    def get_pressure(self, obj: limb) -> float:
        obj1, obj2 = self.get_obj(obj)
        pressure_tl = obj1.ltop_mean
        pressure_tr = obj1.rtop_mean 
        pressure_bl = obj1.lbottom_mean
        pressure_br = obj1.rbottom_mean
        return pressure_tl, pressure_tr, pressure_bl, pressure_br

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