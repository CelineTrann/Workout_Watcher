import ImageProcessing.process_data as pd
from enum import Enum

class distance(Enum):
    CLOSER_X = "closer together horizontally",
    FURTHER_X = "further away horizontally", 
    CLOSER_Y = "closer together vertically",
    FURTHER_Y = "further away vertically",
    PERFECT = "Perfect!"

class rotation(Enum):
    CLOSER_LEFT = "on your left side closer to your body",
    FURTHER_LEFT = "on your left side away from your body", 
    CLOSER_RIGHT = "on your right side closer to your body",
    FURTHER_RIGHT = "on your right side away from your body",
    PERFECT = "Perfect!",
    PERPENDICULAR_LEFT = 'on your left side 90 degrees',
    PERPENDICULAR_RIGHT = 'on your right side 90 degrees'

def print_distance_results(results: dict, obj: pd.limb) -> None:
    if results[distance.PERFECT.name]:
        print(f"{distance.PERFECT.value}")
        return
    
    obj_name = obj.get_plural_hand if obj == pd.limb.HAND else obj.get_plural_foot

    if results[distance.CLOSER_X.name]:
        print(f'Move your {obj_name} {distance.CLOSER_X.value}.')
    elif results[distance.FURTHER_X.name]:
        print(f'Move your {obj_name} {distance.FURTHER_X.value}.')

    if results[distance.CLOSER_Y.name]:
        print(f'Move your {obj_name} {distance.CLOSER_Y.value}.')
    elif results[distance.FURTHER_Y.name]:
        print(f'Move your {obj_name} {distance.FURTHER_Y.value}.')

def print_rotation_results(results: dict, obj: pd.limb) -> None:
    if results[rotation.PERFECT.name]:
        print(f"{rotation.PERFECT.value}")
        return

    if results[rotation.CLOSER_LEFT.name]:
        print(f'Rotate your {obj.name} {rotation.CLOSER_LEFT.value}.')
    elif results[rotation.FURTHER_LEFT.name]:
        print(f'Rotate your {obj.name} {rotation.FURTHER_LEFT.value}.')
    elif results[rotation.PERPENDICULAR_LEFT.name]:
        print(f'Rotate your {obj.name} {rotation.PERPENDICULAR_LEFT.value}.')

    if results[rotation.CLOSER_RIGHT.name]:
        print(f'Rotate your {obj.name} {rotation.CLOSER_RIGHT.value}.')
    elif results[rotation.FURTHER_LEFT.name]:
        print(f'Rotate your {obj.name} {rotation.FURTHER_RIGHT.value}.')
    elif results[rotation.PERPENDICULAR_RIGHT.name]:
        print(f'Rotate your {obj.name} {rotation.PERPENDICULAR_RIGHT.value}.')


def closer_distance(data: pd.Boxes, obj: pd.limb, ux, lx, uy, ly, tol) -> dict:
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
        correction[distance.CLOSER_Y.name] = True
    elif foot_distance_y - tol < ly:
        correction[distance.PERFECT.name] =  False
        correction[distance.FURTHER_Y.name] = True
    
    return correction

def closer_rotation(data: pd.Boxes, obj: pd.limb, l_rot, r_rot, tol) -> dict:
    left, right = data.get_sides(obj)
    correction = {
        rotation.PERFECT.name: True,
        rotation.CLOSER_LEFT.name: False, 
        rotation.FURTHER_LEFT.name: False,
        rotation.CLOSER_RIGHT.name: False,
        rotation.FURTHER_RIGHT.name: False,
        rotation.PERPENDICULAR_RIGHT.name: False,
        rotation.PERPENDICULAR_LEFT.name: False
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

def closer_rotation_tree(data: pd.Boxes, obj_side: pd.side, rot, tol):
    correction = {
        rotation.PERFECT.name: True,
        rotation.CLOSER_LEFT.name: False, 
        rotation.FURTHER_LEFT.name: False,
        rotation.CLOSER_RIGHT.name: False,
        rotation.FURTHER_RIGHT.name: False,
        rotation.PERPENDICULAR_RIGHT.name: False,
        rotation.PERPENDICULAR_LEFT.name: False
    }

    foot = data.feet[0]
    if foot.get_rotation() > rot + tol and foot.get_rotation() < 90:
        correction[rotation.PERFECT.name] = False
        if obj_side == pd.side.LEFT:
            correction[rotation.CLOSER_LEFT.name] = True
        else: 
            correction[rotation.FURTHER_RIGHT.name] = True
            
    elif foot.get_rotation() > rot + tol and foot.get_rotation() > 90:
        correction[rotation.PERFECT.name] = False
        if obj_side == pd.side.LEFT:
            correction[rotation.FURTHER_LEFT.name] = True
        else: 
            correction[rotation.CLOSER_RIGHT.name] = True
            
    elif foot.get_rotation() == 90:
        correction[rotation.PERFECT.name] = False
        if obj_side == pd.side.LEFT:
            correction[rotation.PERPENDICULAR_LEFT.name] = True
        else:
            correction[rotation.PERPENDICULAR_RIGHT.name] = True
            
    return correction

def correct_tree(data: pd.Boxes, obj_side: pd.side):
    correct_rotation = closer_rotation_tree(data, pd.limb.FOOT, 0, 5)

    print_rotation_results(correct_rotation, pd.limb.FOOT)

def correct_warrior1(data: pd.Boxes, l_rot, r_rot):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)

    print_distance_results(correct_distance, pd.limb.FOOT)
    print_rotation_results(correct_rotation, pd.limb.FOOT)

def correct_downwardDog(data: pd.Boxes):
    correct_distance_feet = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_distance_hands = closer_distance(data, pd.limb.HAND, 0, 0, 0, 0)

    correct_rotation_feet = closer_rotation(data, pd.limb.FOOT, 0, 0, 5)
    correct_rotation_hand = closer_rotation(data, pd.limb.HAND, 0, 0, 5)

    print_distance_results(correct_distance_feet, pd.limb.FOOT)
    print_distance_results(correct_distance_hands, pd.limb.HAND)

    print_rotation_results(correct_rotation_feet, pd.limb.FOOT)
    print_rotation_results(correct_rotation_hand, pd.limb.HAND)
    

def correct_triangle(data: pd.Boxes, l_rot, r_rot):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)

    print_distance_results(correct_distance, pd.limb.FOOT)
    print_rotation_results(correct_rotation, pd.limb.FOOT)