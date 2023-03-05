import ImageProcessing.process_data as pd
import correct_pose as cp
import time

def check_distance(data: pd.Boxes, obj: pd.limb, ux, lx, uy, ly, tol) -> bool:
    '''
    Key Arguments:
    data: current boxes
    obj: hands or feet
    ux: upper limit of distances between obj on x-axis
    lx: lower limit of distances between obj on x-axis
    uy: upper limit of distances between obj on y-axis
    ly: lower limit of distances between obj on y-axis
    '''
    foot_distance_x, foot_distance_y = data.get_distance(obj)
    if foot_distance_x + tol > ux or foot_distance_x - tol < lx:
        return False
    elif foot_distance_y + tol > uy or foot_distance_y - tol < ly:
        return False
    
    return True

def set_label(data: pd.Boxes, expected_obj: int) -> None:
    objs = data.no_label
    if len(objs) > expected_obj:
        return False
    
    elif expected_obj > 2:
        # set hand labels for at the top of the map
        objs.sort(key = lambda x: x.centroid_y, reverse=False)
        for _ in range(2):
            print('label hand')
            curr_obj = objs.pop()
            curr_obj.set_label(pd.limb.HAND.value)
            data.hands.append(curr_obj)

    for _ in range(len(objs)):
        print('label foot')
        curr_obj = objs.pop()
        curr_obj.set_label(pd.limb.FOOT.value)
        data.feet.append(curr_obj)

    return True

def check_rotation(data: pd.Boxes, obj: pd.limb, l_rot, r_rot, tol):
    left, right = data.get_sides(obj)
    if left.get_rotation > l_rot + tol or left.get_rotation < l_rot - tol:
        return False
    elif right.get_rotation > r_rot + tol or right.get_rotation < r_rot - tol:
        return False
    
    return True
    
# Function returns if pose is 90% correct
def check_tree(data: pd.Boxes, obj_side: pd.side) -> None:
    if not set_label(data, 1):
        return 
    
    foot = data.feet[0]
    foot.set_side(obj_side)

    hold_pose = True

    if foot.get_rotation() > 0 + 5 or foot.get_rotation() < 0 - 5:
        correct_rotation = cp.closer_rotation_tree(data, pd.limb.FOOT, 0, 5)
        cp.print_rotation_results(correct_rotation, pd.limb.FOOT)
        hold_pose = False

    if hold_pose:
        print("Hold pose")
        time.sleep(10)
    else:
        time.sleep(5)


def check_warrior1(data: pd.Boxes, l_rot, r_rot) -> None:
    if not set_label(data, 2):
        return False
    
    data.set_side(pd.limb.FOOT)

    hold_pose = True
    if not check_distance(data, pd.limb.FOOT, 14, 18, 18, 22, 3):
        correct_distance = cp.closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
        cp.print_distance_results(correct_distance, pd.limb.FOOT)
        hold_pose = False
    
    elif not check_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5):
        correct_rotation = cp.closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)
        cp.print_rotation_results(correct_rotation, pd.limb.FOOT)
        hold_pose = False
    
    if hold_pose:
        print("Hold pose")
        time.sleep(10)
    else:
        time.sleep(5)
    

def check_downwardDog(data: pd.Boxes) -> None:
    if not set_label(data, 4):
        return 
    
    data.set_side(pd.limb.FOOT)
    data.set_side(pd.limb.HAND)

    hold_pose = True

    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0, 0):
        correct_distance_feet = cp.closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
        cp.print_distance_results(correct_distance_feet, pd.limb.FOOT)
        hold_pose = False
    elif not check_distance(data, pd.limb.HAND, 0, 0, 0, 0, 0):
        correct_distance_hands = cp.closer_distance(data, pd.limb.HAND, 0, 0, 0, 0)
        cp.print_distance_results(correct_distance_hands, pd.limb.HAND)
        hold_pose = False
    
    elif not check_rotation(data, pd.limb.FOOT, 0, 0, 5):
        correct_rotation_feet = cp.closer_rotation(data, pd.limb.FOOT, 0, 0, 5)
        cp.print_rotation_results(correct_rotation_feet, pd.limb.FOOT)
        hold_pose = False
    elif not check_rotation(data, pd.limb.HAND, 0, 0, 5):
        correct_rotation_hand = cp.closer_rotation(data, pd.limb.HAND, 0, 0, 5)
        cp.print_rotation_results(correct_rotation_hand, pd.limb.HAND)
        hold_pose = False
    
    if hold_pose:
        print("Hold pose")
        time.sleep(10)
    else:
        time.sleep(5)


def check_triangle(data: pd.Boxes, l_rot, r_rot) -> None:
    if not set_label(data, 2):
        return 
    
    data.set_side(pd.limb.FOOT)
    
    hold_pose = True
    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0, 0):
        correct_distance = cp.closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0)
        hold_pose = False
    
    elif not check_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5):
        correct_rotation = cp.closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)
        hold_pose = False
    
    if hold_pose:
        print("Hold pose")
        time.sleep(10)
    else:
        time.sleep(5)
    
    