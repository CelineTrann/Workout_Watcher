import ImageProcessing.process_data as pd
import correct_pose as cp
import time
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestore

# initializations 
cred = credentials.Certificate("workoutwatcher-654cd-firebase-adminsdk-xkutc-a7c0fc0bc5.json")
# firebase_admin.initialize_app(cred)

#firebase_admin.initialize_app(cred)
db = firestore.client()

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

def check_rotation(data: pd.Boxes, obj: pd.limb, l_rot, r_rot, tol):
    left, right = data.get_sides(obj)
    print("Detected angle: left - %s, right - %s"%(left.get_rotation(), right.get_rotation()))
    if left.get_rotation() > l_rot + tol or left.get_rotation() < l_rot - tol:
        return False
    
    elif right.get_rotation() > r_rot + tol or right.get_rotation() < r_rot - tol:
        return False
    
    return True

def check_pressure(data: pd.Boxes, pressure, pose) -> bool:
    '''
    Key Arguments:
    data: current boxes
    obj: hands or feet
    up: upper limit of pressure
    lp: lower limit of pressure 
    buff: leeway for pressure
    '''

    if pose == 'Right Tree Pose' and data.feet[0]:
        if data.feet[0].rtop_mean > data.feet[0].ltop_mean and data.feet[0].rtop_mean > data.feet[0].rbottom_mean and data.feet[0].rtop_mean > data.feet[0].lbottom_mean:
            return True
        else:  
            if pose == 'Left Tree Pose' and data.feet[0]:
                if data.feet[0].rtop_mean < data.feet[0].ltop_mean and data.feet[0].rtop_mean < data.feet[0].rbottom_mean and data.feet[0].rtop_mean < data.feet[0].lbottom_mean:
                    return True
                else: 
                    return False
              
    if pose == 'Left Warrior 1 Pose': #left
        pressure_tl, pressure_tr, pressure_bl, pressure_br, pressure_tlo, pressure_tro, pressure_blo, pressure_bro = data.get_pressure(pd.limb.FOOT)        
        if pressure_bro < pressure_tro and pressure_bro < pressure_tlo and pressure_bro < pressure_blo:
            return True
    else: 
        if pose == 'Right Warrior 1 Pose': #right
            if pressure_blo < pressure_tlo and pressure_blo < pressure_tro and pressure_blo < pressure_bro:
                return True
            else: 
                return False

 #   if pose == 'downwardDog':
 #       pressure_tl, pressure_tr, pressure_bl, pressure_br, pressure_tlo, pressure_tro, pressure_blo, pressure_bro = data.get_pressure(pd.limb.FOOT)
 #       pressure_tla, pressure_tra, pressure_bla, pressure_bra, pressure_tlb, pressure_trb, pressure_blb, pressure_brb = data.get_pressure(pd.limb.HAND)
 #       if pressure_tr == pressure.HIGH and pressure_tl == pressure.HIGH and pressure_tro == pressure.HIGH and pressure_tlo == pressure.HIGH: 
 #           if pressure_bla == pressure.HIGH and pressure_bra == pressure.HIGH and pressure_blb and pressure_brb:
 #               return True
 #           else:
 #               return False

    if pose == 'Left Triangle Pose': #left
        pressure_tl, pressure_tr, pressure_bl, pressure_br, pressure_tlo, pressure_tro, pressure_blo, pressure_bro = data.get_pressure(pd.limb.FOOT)
        if pressure_bro < pressure_blo and pressure_bro < pressure_tro and pressure_bro < pressure_tlo:
            return True
    else:                             
        if pose == 'Right Triangle Pose': #right
            if pressure_blo < pressure_bro and pressure_blo < pressure_tlo and pressure_blo < pressure_tro:
                return True
            else:
                return False  
                 
def check_tree(data: pd.Boxes, obj_side: pd.side) -> None:
    if not set_label(data, 1):
        print("Early return.")
        return 
    
    foot = data.feet[0]
    foot.set_side(obj_side)

    hold_pose = True

    print("Angle for tree is: %s"%foot.get_rotation())
    if foot.get_rotation() > 0 + 5 or foot.get_rotation() < 0 - 5:
        print("Rotation is incorrect.")
        correct_rotation = cp.closer_rotation_tree(data, pd.limb.FOOT, 0, 5)
        cp.print_rotation_results(correct_rotation, pd.limb.FOOT)
        hold_pose = False
  
    if not check_pressure(data, pd.limb.FOOT, 'tree'):
        correct_pressure = cp.closer_pressure_tree(data)
        cp.print_pressure_results(correct_pressure, pd.limb.FOOT, obj_side)
        hold_pose = False

    if hold_pose:
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        doc_ref.update({
       'isPoseCorrect': True
       })
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
        correct_distance = cp.closer_distance(data, pd.limb.FOOT, 14, 18, 18, 22, 3)
        hold_pose = False
        cp.print_distance_results(correct_distance, pd.limb.FOOT)
    
    if not check_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5):
        correct_rotation = cp.closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)
        hold_pose = False
        cp.print_rotation_results(correct_rotation, pd.limb.FOOT)
    
    if not check_pressure(data, pd.limb.FOOT, 'left warrior1' or 'right warrior1'):
        correct_pressure_left, correct_pressure_right = cp.closer_pressure(data, pd.limb.FOOT,
            pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH)
        hold_pose = False
        cp.print_pressure_results(correct_pressure_left, pd.limb.FOOT, pd.side.LEFT)
        cp.print_pressure_results(correct_pressure_right, pd.limb.FOOT, pd.side.RIGHT)

    if hold_pose:
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        doc_ref.update({
       'isPoseCorrect': True
       })
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
        correct_distance_feet = cp.closer_distance(data, pd.limb.FOOT, 0, 0, 0, 0, 0)
        cp.print_distance_results(correct_distance_feet, pd.limb.FOOT)
        hold_pose = False
    elif not check_distance(data, pd.limb.HAND, 0, 0, 0, 0, 0):
        correct_distance_hands = cp.closer_distance(data, pd.limb.HAND, 0, 0, 0, 0, 0)
        cp.print_distance_results(correct_distance_hands, pd.limb.HAND)
        hold_pose = False
    
    if not check_rotation(data, pd.limb.FOOT, 0, 0, 5):
        correct_rotation_feet = cp.closer_rotation(data, pd.limb.FOOT, 0, 0, 5)
        cp.print_rotation_results(correct_rotation_feet, pd.limb.FOOT)
        hold_pose = False
    elif not check_rotation(data, pd.limb.HAND, 0, 0, 5):
        correct_rotation_hand = cp.closer_rotation(data, pd.limb.HAND, 0, 0, 5)
        cp.print_rotation_results(correct_rotation_hand, pd.limb.HAND)
        hold_pose = False

    if not check_pressure(data, pd.limb.FOOT, 'downwardDog'):
        correct_pressure_left, correct_pressure_right = cp.closer_pressure(data, pd.limb.FOOT, 
            pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH)
        cp.print_pressure_results(correct_pressure_left, pd.limb.FOOT, pd.side.LEFT)
        cp.print_pressure_results(correct_pressure_right, pd.limb.FOOT, pd.side.RIGHT)
        hold_pose = False
    elif not check_pressure(data, pd.limb.FOOT, 'downwardDog'):
        correct_pressure_left, correct_pressure_right = cp.closer_pressure(data, pd.limb.HAND, 
            pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH)
        cp.print_pressure_results(correct_pressure_left, pd.limb.HAND, pd.side.LEFT)
        cp.print_pressure_results(correct_pressure_right, pd.limb.HAND, pd.side.RIGHT)
        hold_pose = False
    
    if hold_pose:
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        doc_ref.update({
       'isPoseCorrect': True
       })
        print("Hold pose")
        time.sleep(10)
    else:
        time.sleep(5)


def check_triangle(data: pd.Boxes, l_rot, r_rot) -> None:
    if not set_label(data, 2):
        return 
    
    data.set_side(pd.limb.FOOT)
    
    hold_pose = True
    if not check_distance(data, pd.limb.FOOT, 0, 0, 18, 22, 3):
        correct_distance = cp.closer_distance(data, pd.limb.FOOT, 0, 0, 18, 22, 3)
        cp.print_distance_results(correct_distance, pd.limb.FOOT)
        hold_pose = False
    
    if not check_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5):
        correct_rotation = cp.closer_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5)
        cp.print_rotation_results(correct_rotation, pd.limb.FOOT)
        hold_pose = False

    if not check_pressure(data, pd.limb.FOOT, 'left triangle' or 'right triangle'):
        correct_pressure_left, correct_pressure_right = cp.closer_pressure(data, pd.limb.FOOT,
            pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH, pd.pressure.HIGH)
        cp.print_pressure_results(correct_pressure_left, pd.limb.FOOT, pd.side.LEFT)
        cp.print_pressure_results(correct_pressure_right, pd.limb.FOOT, pd.side.RIGHT)
        hold_pose = False
    
    if hold_pose:
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        doc_ref.update({
       'isPoseCorrect': True
       })
        print("Hold pose")
        time.sleep(10)
    else:
        time.sleep(5)
    
    
