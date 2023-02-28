import ImageProcessing.process_data as pd
from enum import Enum

class distance(Enum):
    CLOSER_X = "closer together horizontally",
    FURTHER_X = "further away horizontally", 
    CLOSER_Y = "closer together vertically",
    FURTHER_Y = "further away vertically",
    PERFECT = 4

class rotation(Enum):
    CLOSER_LEFT = 0,
    FURTHER_LEFT = 1, 
    CLOSER_RIGHT = 2,
    FURTHER_RIGHT = 3,
    PERFECT = 4

def closer_distance(data: pd.Boxes, obj: pd.limb, ux, lx, uy, ly, tol) -> dict[distance.name, bool]:
    foot_distance_x, foot_distance_y = data.get_distance(obj)
    correction = {
        distance.PERFECT.name: True,
        distance.CLOSER_X.name: False, 
        distance.FURTHER_X.name: False,
        distance.CLOSER_Y.name: False,
        distance.FURTHER_Y.name: False
    }

    if foot_distance_x + tol > ux:
        correction[distance.PERFECT.name] =  False
        correction[distance.CLOSER_X.name] = True
    elif foot_distance_x - tol < lx:
        correction[distance.PERFECT.name] =  False
        correction[distance.FURTHER_X.name] = True
    
    if foot_distance_y + tol > uy:
        correction[distance.PERFECT.name] =  False
        correction[distance.CLOSER_Y. name] = True
    elif foot_distance_y - tol < ly:
        correction[distance.PERFECT.name] =  False
        correction[distance.FURTHER_Y.name] = True
    
    return correction

def closer_rotation(data: pd.Boxes, obj: pd.limb, l_rot, r_rot, tol) -> dict[rotation.name, bool]:
    left, right = data.get_sides(obj)
    correction = {
        rotation.PERFECT.name: True,
        rotation.CLOSER_LEFT.name: False, 
        rotation.FURTHER_LEFT.name: False,
        rotation.CLOSER_RIGHT.name: False,
        rotation.FURTHER_RIGHT.name: False
    }

    if left.get_rotation > l_rot + tol:
        correction[rotation.PERFECT.name] = False
        correction[rotation.CLOSER_LEFT.name] = True
    elif left.get_rotation < l_rot - tol:
        correction[rotation.PERFECT.name] = False
        correction[rotation.FURTHER_LEFT.name] = True
    
    if right.get_rotation > r_rot + tol:
        correction[rotation.PERFECT.name] = False
        correction[rotation.FURTHER_RIGHT.name] = True
    elif right.get_rotation < r_rot - tol:
        correction[rotation.PERFECT.name] = False
        correction[rotation.CLOSER_RIGHT.name] = True
    
    return correction

def correct_tree(data: pd.Boxes):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, 0, 0, 5)

def correct_warrior1(data: pd.Boxes, l_rot, r_rot):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)

def correct_downwardDog(data: pd.Boxes):
    correct_distance_feet = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_distance_hands = closer_distance(data, pd.limb.HAND, 0, 0, 0, 0)

    correct_rotation_feet = closer_rotation(data, pd.limb.FOOT, 0, 0, 5)
    correct_rotation_hand = closer_rotation(data, pd.limb.HAND, 0, 0, 5)
    

def correct_triangle(data: pd.Boxes, l_rot, r_rot):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)