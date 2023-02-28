import ImageProcessing.process_data as pd
from enum import Enum

class distance(Enum):
    CLOSER_X = 0,
    FURTHER_X = 1, 
    CLOSER_Y = 2,
    FURTHER_Y = 3,
    PERFECT = 4

class rotation(Enum):
    CLOSER_LEFT = 0,
    FURTHER_LEFT = 1, 
    CLOSER_RIGHT = 2,
    FURTHER_RIGHT = 3,
    PERFECT = 4

closer = {}
closer[distance.CLOSER_X] = 1
print(closer)

def closer_distance(data: pd.Boxes, obj: pd.limb, ux, lx, uy, ly, tol):
    foot_distance_x, foot_distance_y = data.get_distance(obj)
    correction = {}
    if foot_distance_x + tol > ux:
        correction[distance.CLOSER_X.name] = 0
    elif foot_distance_x - tol < lx:
        return distance.FURTHER_X
    elif foot_distance_y + tol > uy:
        return distance.CLOSER_Y
    elif foot_distance_y - tol < ly:
        return distance.FURTHER_Y
    
    return distance.PERFECT

def closer_rotation(data: pd.Boxes, obj: pd.limb, l_rot, r_rot, tol):
    left, right = data.get_sides(obj)
    if left.get_rotation > l_rot + tol or left.get_rotation < l_rot - tol:
        return False
    elif right.get_rotation > r_rot + tol or right.get_rotation < r_rot - tol:
        return False
    
    return True

def correct_tree():
    pass

def correct_warrior1():
    pass

def correct_downwardDog():
    pass

def correct_triangle():
    pass