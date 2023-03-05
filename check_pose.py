import ImageProcessing.process_data as pd

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

def check_pressure(data: pd.Boxes, obj: pd.limb, pressure, buff, pose) -> bool:
    '''
    Key Arguments:
    data: current boxes
    obj: hands or feet
    up: upper limit of pressure
    lp: lower limit of pressure 
    buff: leeway for pressure
    '''

    if pose == 'tree' and data.feet[0]:
        pressure_tl, pressure_tr, pressure_bl, pressure_br, pressure_tlo, pressure_tro, pressure_blo, pressure_bro = data.get_pressure_feet(obj)
        if pressure_tl == pressure.HIGH and pressure_tr == pressure.HIGH and pressure_bl == pressure.HIGH and pressure_br == pressure.HIGH:
            return True
        else: 
            return False
              
    if pose == 'left warrior1': #left
        pressure_tl, pressure_tr, pressure_bl, pressure_br, pressure_tlo, pressure_tro, pressure_blo, pressure_bro = data.get_pressure_feet(obj)        
        if  pressure_tr == pressure.HIGH and pressure_tl == pressure.HIGH:
            if pressure_tro == pressure.HIGH and pressure_tlo == pressure.HIGH and pressure_bro == pressure.HIGH:
                return True
            else: 
                if pose == 'right warrior1': #right
                    if pressure_tro == pressure.HIGH and pressure_tlo == pressure.HIGH:
                        if pressure_tr == pressure.HIGH and pressure_tl == pressure.HIGH and pressure_bl == pressure.HIGH:
                            return True
                        else: 
                            return False

    if pose == 'downwardDog':
        pressure_tl, pressure_tr, pressure_bl, pressure_br, pressure_tlo, pressure_tro, pressure_blo, pressure_bro = data.get_pressure_feet(obj)
        pressure_tla, pressure_tra, pressure_bla, pressure_bra, pressure_tlb, pressure_trb, pressure_blb, pressure_brb = data.get_pressure_hands(obj)
        if pressure_tr == pressure.HIGH and pressure_tl == pressure.HIGH and pressure_tro == pressure.HIGH and pressure_tlo == pressure.HIGH: 
            if pressure_bla == pressure.HIGH and pressure_bra == pressure.HIGH and pressure_blb and pressure_brb:
                return True
            else:
                return False

    if pose == 'left triangle': #left
        pressure_tl, pressure_tr, pressure_bl, pressure_br, pressure_tlo, pressure_tro, pressure_blo, pressure_bro = data.get_pressure_feet(obj)
        if pressure_tl == pressure.MEDIUM and pressure_tr == pressure.MEDIUM and pressure_bl == pressure.MEDIUM and pressure_br == pressure.MEDIUM:
            if pressure_br == pressure.HIGH and pressure_bl == pressure.HIGH:
                return True
            else:                             
                if pose == 'right triangle': #right
                    if pressure_tl == pressure.MEDIUM and pressure_tr == pressure.MEDIUM and pressure_bl == pressure.MEDIUM and pressure_br == pressure.MEDIUM:
                        if pressure_br == pressure.HIGH and pressure_bl == pressure.HIGH:
                            return True
                        else:
                            return False  

                 

def check_rotation(data: pd.Boxes, obj: pd.limb, l_rot, r_rot, tol):
    left, right = data.get_sides(obj)
    if left.get_rotation > l_rot + tol or left.get_rotation < l_rot - tol:
        return False
    
    elif right.get_rotation > r_rot + tol or right.get_rotation < r_rot - tol:
        return False
    
    return True

# Function returns if pose is 90% correct
def check_tree(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)

    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    
    elif not check_rotation(data, pd.limb.FOOT, 0, 0, 5):
        return False
    
    elif not check_pressure(data, pd.limb.FOOT, 0, 0, 0, 'tree'):
        return False
  
    return True 

def check_warrior1(data: pd.Boxes, l_rot, r_rot) -> bool:
    data.set_side(pd.limb.FOOT)

    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    
    elif not check_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5):
        return False
    
    elif not check_pressure(data, pd.limb.FOOT, 0, 0, 'left warrior1' or 'right warrior1'):
        return False 

def check_downwardDog(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    data.set_side(pd.limb.HAND)

    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    
    elif not check_distance(data, pd.limb.HAND, 0, 0, 0, 0):
        return False
    
    elif not check_rotation(data, pd.limb.FOOT, 0, 0, 5):
        return False
    
    elif not check_rotation(data, pd.limb.HAND, 0, 0, 5):
        return False
    
    elif not check_pressure(data, pd.limb.FOOT, 0, 0, 'downwardDog'):
        return False

def check_triangle(data: pd.Boxes, l_rot, r_rot) -> bool:
    data.set_side(pd.limb.FOOT)
    
    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    
    elif not check_rotation(data, pd.limb.FOOT, l_rot, r_rot, 5):
        return False

    elif not check_pressure(data, pd.limb.FOOT, 0, 0, 'left triangle' or 'right triangle'):
        return False