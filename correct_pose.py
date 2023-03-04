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
    PERFECT = "Perfect!"

class pressure(Enum):
    LESS_PRESSURE_LEFTTOP = "Apply less pressure on the top left side of your ",
    MORE_PRESSURE_LEFTTOP = "Apply more pressure on the top left side of your", 
    LESS_PRESSURE_LEFTBOTTOM = "Apply less pressure on the bottom left side of your",
    MORE_PRESSURE_LEFTBOTTOM = "Apply more pressure on the bottom left side of your",
    LESS_PRESSURE_RIGHTTOP = "Apply less pressure on the top right side of your",
    MORE_PRESSURE_RIGHTTOP = "Apply more pressure on the top right side of your",
    LESS_PRESSURE_RIGHTBOTTOM = "Apply less pressure on the bottom right side of your",
    MORE_PRESSURE_RIGHTBOTTOM = "Apply more pressure on the bottom right side of your",
    PERFECT = "Perfect!"

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
        print(f'Rotate your {obj} {rotation.CLOSER_LEFT.value}.')
    elif results[rotation.FURTHER_LEFT.name]:
        print(f'Rotate your {obj} {rotation.FURTHER_LEFT.value}.')

    if results[rotation.CLOSER_RIGHT.name]:
        print(f'Rotate your {obj} {rotation.CLOSER_RIGHT.value}.')
    elif results[rotation.FURTHER_LEFT.name]:
        print(f'Rotate your {obj} {rotation.FURTHER_RIGHT.value}.')

def print_pressure_results(results: dict, obj: pd.limb) -> None:
    if results[pressure.PERFECT.name]:
        print(f"{pressure.PERFECT.value}")
        return

    if results[pressure.LESS_PRESSURE_LEFTTOP.name]:
        print(f'{pressure.LESS_PRESSURE_LEFTTOP.value} {obj}.')
    elif results[pressure.MORE_PRESSURE_LEFTTOP.name]:
        print(f'{pressure.MORE_PRESSURE_LEFTTOP.value} {obj}.')
    elif results[pressure.LESS_PRESSURE_LEFTBOTTOM.name]:
        print(f'{pressure.LESS_PRESSURE_LEFTBOTTOM.value} {obj}.')
    elif results[pressure.MORE_PRESSURE_LEFTBOTTOM.name]:
        print(f'{pressure.MORE_PRESSURE_LEFTBOTTOM.value} {obj}.')

    if results[pressure.LESS_PRESSURE_RIGHTTOP.name]:
        print(f'{pressure.LESS_PRESSURE_RIGHTTOP.value} {obj}.')
    elif results[pressure.MORE_PRESSURE_RIGHTTOP.name]:
        print(f'{pressure.MORE_PRESSURE_RIGHTTOP.value} {obj}.')
    elif results[pressure.LESS_PRESSURE_RIGHTBOTTOM.name]:
        print(f'{pressure.LESS_PRESSURE_RIGHTBOTTOM.value} {obj}.')
    elif results[pressure.MORE_PRESSURE_RIGHTBOTTOM.name]:
        print(f'{pressure.MORE_PRESSURE_RIGHTBOTTOM.value} {obj}.')

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

def closer_pressure(data: pd.Boxes, obj: pd.limb, up, lp, buff) -> dict:
    foot_pressure_tl, foot_pressure_tr, foot_pressure_bl, foot_pressure_br = data.get_pressure(obj)
    correction = {
        pressure.PERFECT.name: True,
        pressure.LESS_PRESSURE_LEFTTOP.name: False, 
        pressure.MORE_PRESSURE_LEFTTOP.name: False,
        pressure.LESS_PRESSURE_LEFTBOTTOM.name: False, 
        pressure.MORE_PRESSURE_LEFTBOTTOM.name: False,
        pressure.LESS_PRESSURE_RIGHTTOP.name: False,
        pressure.MORE_PRESSURE_RIGHTTOP.name: False,
        pressure.LESS_PRESSURE_RIGHTBOTTOM.name: False,
        pressure.MORE_PRESSURE_RIGHTBOTTOM.name: False
    }

    if foot_pressure_tl > up + buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.LESS_PRESSURE_LEFTTOP.name] = True
    elif foot_pressure_tl < lp - buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_LEFTTOP.name] = True
    
    if foot_pressure_tr > up + buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.LESS_PRESSURE_RIGHTTOP.name] = True
    elif foot_pressure_tr < lp - buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_RIGHTTOP.name] = True

    if foot_pressure_bl > up + buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.LESS_PRESSURE_LEFTBOTTOM.name] = True
    elif foot_pressure_bl < lp - buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_LEFTBOTTOM.name] = True

    if foot_pressure_br > up + buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.LESS_PRESSURE_RIGHTBOTTOM.name] = True
    elif foot_pressure_br < lp - buff:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_RIGHTBOTTOM.name] = True

    return correction

def correct_tree(data: pd.Boxes):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, 0, 0, 5)
    correct_pressure = closer_pressure(data, pd.limb, 0, 0, 0)

    print_distance_results(correct_distance, pd.limb.FOOT)
    print_rotation_results(correct_rotation, pd.limb.FOOT)
    print_pressure_results(correct_pressure, pd.limb, 0, 0, 0)

def correct_warrior1(data: pd.Boxes, l_rot, r_rot):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)
    correct_pressure = closer_pressure(data, pd.limb, 0, 0, 0)

    print_distance_results(correct_distance, pd.limb.FOOT)
    print_rotation_results(correct_rotation, pd.limb.FOOT)
    print_pressure_results(correct_pressure, pd.limb, 0, 0, 0)


def correct_downwardDog(data: pd.Boxes):
    correct_distance_feet = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_distance_hands = closer_distance(data, pd.limb.HAND, 0, 0, 0, 0)

    correct_rotation_feet = closer_rotation(data, pd.limb.FOOT, 0, 0, 5)
    correct_rotation_hand = closer_rotation(data, pd.limb.HAND, 0, 0, 5)

    correct_pressure_feet = closer_pressure(data, pd.limb.FOOT, 0, 0, 0)
    correct_pressure_hand = closer_pressure(data, pd.limb.HAND, 0, 0, 0)

    print_distance_results(correct_distance_feet, pd.limb.FOOT)
    print_distance_results(correct_distance_hands, pd.limb.HAND)

    print_rotation_results(correct_rotation_feet, pd.limb.FOOT)
    print_rotation_results(correct_rotation_hand, pd.limb.HAND)
    
    print_pressure_results(correct_pressure_feet, pd.limb.FOOT)
    print_pressure_results(correct_pressure_hand, pd.limb.HAND)

def correct_triangle(data: pd.Boxes, l_rot, r_rot):
    correct_distance = closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
    correct_rotation = closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)
    correct_pressure = closer_pressure(data, pd.limb, 0, 0, 0)

    print_distance_results(correct_distance, pd.limb.FOOT)
    print_rotation_results(correct_rotation, pd.limb.FOOT)
    print_pressure_results(correct_pressure, pd.limb, 0, 0, 0)
