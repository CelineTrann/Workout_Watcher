import ImageProcessing.process_data as pd
from enum import Enum, IntEnum
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore
import time

#from google.cloud import firestore

# initializations 
cred = credentials.Certificate("workoutwatcher-654cd-firebase-adminsdk-xkutc-a7c0fc0bc5.json")
firebase_admin.initialize_app(cred)

#firebase_admin.initialize_app(cred)
db = firestore.client()

class distance(Enum):
    CLOSER_X = "closer together horizontally",
    FURTHER_X = "further away horizontally", 
    CLOSER_Y = "closer together vertically",
    FURTHER_Y = "further away vertically",
    PERFECT = "Distance Perfect!"

class rotation(Enum):
    CLOSER_LEFT = "on your left side closer to your body",
    FURTHER_LEFT = "on your left side away from your body", 
    CLOSER_RIGHT = "on your right side closer to your body",
    FURTHER_RIGHT = "on your right side away from your body",
    PERFECT = "Rotation Perfect!",
    PERPENDICULAR_LEFT = 'on your left side 90 degrees',
    PERPENDICULAR_RIGHT = 'on your right side 90 degrees'

class pressure(Enum):
    LESS_PRESSURE_LEFTTOP = "Apply less pressure on the top left side of your ",
    MORE_PRESSURE_LEFTTOP = "Apply more pressure on the top left side of your", 
    LESS_PRESSURE_LEFTBOTTOM = "Apply less pressure on the bottom left side of your",
    MORE_PRESSURE_LEFTBOTTOM = "Apply more pressure on the bottom left side of your",
    LESS_PRESSURE_RIGHTTOP = "Apply less pressure on the top right side of your",
    MORE_PRESSURE_RIGHTTOP = "Apply more pressure on the top right side of your",
    LESS_PRESSURE_RIGHTBOTTOM = "Apply less pressure on the bottom right side of your",
    MORE_PRESSURE_RIGHTBOTTOM = "Apply more pressure on the bottom right side of your",
    PERFECT = "Pressure Perfect!"

def print_distance_results(results: dict, obj: pd.limb) -> None:
    if results[distance.PERFECT.name]:
        print(f"{distance.PERFECT.value}")
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootDistance':['Left foot is perfect!']
        })
        return
    
    obj_name = obj.get_plural_hand if obj == pd.limb.HAND else obj.get_plural_foot

    if results[distance.CLOSER_X.name]:
        print(f'Move your {obj_name} {distance.CLOSER_X.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootDistance':['Feet closer horizontally']
        })
    elif results[distance.FURTHER_X.name]:
        print(f'Move your {obj_name} {distance.FURTHER_X.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootDistance':['Feet further horizontally']
        })

    if results[distance.CLOSER_Y.name]:
        print(f'Move your {obj_name} {distance.CLOSER_Y.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootDistance': ['Feet closer vertically']
        })
    elif results[distance.FURTHER_Y.name]:
        print(f'Move your {obj_name} {distance.FURTHER_Y.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootDistance':['Feet further vertically']
        })

def print_rotation_clear() -> None:
    doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
    time.sleep(0.3)
    doc_ref.update({
        'leftFootRotation':[''],
        'rightFootRotation':['']
    })

def print_rotation_results(results: dict, obj: pd.limb, sides = 'both') -> None:
    if results[rotation.CLOSER_LEFT.name]:
        print(f'Rotate your {obj.name} {rotation.CLOSER_LEFT.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootRotation':['Rotate left foot closer to body']
        })
    elif results[rotation.FURTHER_LEFT.name]:
        print(f'Rotate your {obj.name} {rotation.FURTHER_LEFT.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootRotation':['Rotate left foot away from body']
        })
    elif results[rotation.PERPENDICULAR_LEFT.name]:
        print(f'Rotate your {obj.name} {rotation.PERPENDICULAR_LEFT.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'leftFootRotation':['Put left foot at 90 degrees']
        })
    elif sides == 'Left' or sides == 'both':
        doc_ref = db.collection(u'users').document(u'1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        doc_ref.update({
            'leftFootRotation':['Left foot is perfect!']
        })

    if results[rotation.CLOSER_RIGHT.name]:
        print(f'Rotate your {obj.name} {rotation.CLOSER_RIGHT.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'rightFootRotation':['Rotate right foot closer to body']
        })
    elif results[rotation.FURTHER_RIGHT.name]:
        print(f'Rotate your {obj.name} {rotation.FURTHER_RIGHT.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'rightFootRotation':['Rotate right foot away from body']
        })
    elif results[rotation.PERPENDICULAR_RIGHT.name]:
        print(f'Rotate your {obj.name} {rotation.PERPENDICULAR_RIGHT.value}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            'rightFootRotation':['Put right foot at 90 degrees']
        })
    elif sides == 'Right' or sides == 'both':
        doc_ref = db.collection(u'users').document(u'1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        doc_ref.update({
        'rightFootRotation':['Right foot is perfect!']
        })

def print_pressure_clear() -> None:
    doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
    time.sleep(0.3)
    doc_ref.update({
        'pressureRightFoot': [''],
        'pressureLeftFoot': ['']
    })

def print_pressure_results(results: dict, obj: pd.limb, obj2: pd.side) -> None:
    if obj2 == pd.side.RIGHT:
        location = 'pressureRightFoot'
    else:
        location = 'pressureLeftFoot'

    if results[pressure.LESS_PRESSURE_LEFTTOP.name]:
        print(f'{pressure.LESS_PRESSURE_LEFTTOP.value} {obj2} {obj}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            location: ['Less pressure on top left']
        })
    elif results[pressure.MORE_PRESSURE_LEFTTOP.name]:
        print(f'{pressure.MORE_PRESSURE_LEFTTOP.value} {obj2} {obj}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            location: ['More pressure on top left']
        })
    elif results[pressure.LESS_PRESSURE_LEFTBOTTOM.name]:
        print(f'{pressure.LESS_PRESSURE_LEFTBOTTOM.value} {obj2} {obj}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            location: ['Less pressure on bottom left']
        })
    elif results[pressure.MORE_PRESSURE_LEFTBOTTOM.name]:
        print(f'{pressure.MORE_PRESSURE_LEFTBOTTOM.value} {obj2} {obj}.')
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            location: ['More pressure on bottom left']
        })
    else: 
        doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        time.sleep(0.3)
        doc_ref.update({
            location:[f'{obj2.value} foot pressure is perfect!']
        })


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

    if left.get_rotation() > l_rot + tol:
        correction[rotation.PERFECT.name] = False
        correction[rotation.CLOSER_LEFT.name] = True
    elif left.get_rotation() < l_rot - tol:
        correction[rotation.PERFECT.name] = False
        correction[rotation.FURTHER_LEFT.name] = True
    
    if right.get_rotation() > r_rot + tol:
        correction[rotation.PERFECT.name] = False
        correction[rotation.FURTHER_RIGHT.name] = True
    elif right.get_rotation() < r_rot - tol:
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

def closer_pressure(data: pd.Boxes, obj: pd.limb, L_tl: pd.pressure, L_tr: pd.pressure, L_bl: pd.pressure, L_br: pd.pressure, R_tl: pd.pressure, R_tr: pd.pressure, R_bl: pd.pressure, R_br: pd.pressure) -> dict:
    L_pressure_tl, L_pressure_tr, L_pressure_bl, L_pressure_br, R_pressure_tl, R_pressure_tr, R_pressure_bl, R_pressure_br = data.get_pressure(obj)
    
    correction_left = {
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

    if L_pressure_tl > L_tl:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.LESS_PRESSURE_LEFTTOP.name] = True
    elif L_pressure_tl < L_tl:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.MORE_PRESSURE_LEFTTOP.name] = True
    
    if L_pressure_tr > L_tr:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.LESS_PRESSURE_RIGHTTOP.name] = True
    elif L_pressure_tr < L_tr:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.MORE_PRESSURE_RIGHTTOP.name] = True

    if L_pressure_bl > L_bl:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.LESS_PRESSURE_LEFTBOTTOM.name] = True
    elif L_pressure_bl < L_bl:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.MORE_PRESSURE_LEFTBOTTOM.name] = True

    if L_pressure_br > L_br:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.LESS_PRESSURE_RIGHTBOTTOM.name] = True
    elif L_pressure_br < L_br:
        correction_left[pressure.PERFECT.name] =  False
        correction_left[pressure.MORE_PRESSURE_RIGHTBOTTOM.name] = True

    correction_right = {
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

    if R_pressure_tl > R_tl:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.LESS_PRESSURE_LEFTTOP.name] = True
    elif R_pressure_tl < R_tl:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.MORE_PRESSURE_LEFTTOP.name] = True
    
    if R_pressure_tr > R_tr:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.LESS_PRESSURE_RIGHTTOP.name] = True
    elif R_pressure_tr < R_tr:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.MORE_PRESSURE_RIGHTTOP.name] = True

    if R_pressure_bl > R_bl:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.LESS_PRESSURE_LEFTBOTTOM.name] = True
    elif R_pressure_bl < R_bl:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.MORE_PRESSURE_LEFTBOTTOM.name] = True

    if R_pressure_br > R_br:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.LESS_PRESSURE_RIGHTBOTTOM.name] = True
    elif R_pressure_br < R_br:
        correction_right[pressure.PERFECT.name] =  False
        correction_right[pressure.MORE_PRESSURE_RIGHTBOTTOM.name] = True

    return correction_left, correction_right

def closer_pressure_tree(data: pd.Boxes) -> dict:
    pressure_tl = data.feet[0].ltop_mean
    pressure_tr = data.feet[0].rtop_mean
    pressure_bl = data.feet[0].lbottom_mean
    pressure_br = data.feet[0].rbottom_mean
    
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

    if pressure_tl < pd.pressure.HIGH:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_LEFTTOP.name] = True
    
    if pressure_tr < pd.pressure.HIGH:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_RIGHTTOP.name] = True

    if pressure_bl < pd.pressure.HIGH:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_LEFTBOTTOM.name] = True

    if pressure_br < pd.pressure.HIGH:
        correction[pressure.PERFECT.name] =  False
        correction[pressure.MORE_PRESSURE_RIGHTBOTTOM.name] = True

    return correction
