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

def check_pressure(data: pd, obj: pd.pressure, up, lp, buff) -> bool:
    '''
    Key Arguments:
    data: current boxes
    obj: hands or feet
    up: upper limit of pressure 
    lp: lower limit of pressure 
    buff: leeway for pressure 
    '''
    foot_pressure_tl, foot_pressure_tr, foot_pressure_bl, foot_pressure_br = data.get_pressure(obj)
    if foot_pressure_tl + buff > up or foot_pressure_tl - buff < lp:
        return False
    elif foot_pressure_tr + buff > up or foot_pressure_tr - buff < lp:
        return False
    elif foot_pressure_bl + buff > up or foot_pressure_bl - buff < lp:
        return False
    elif foot_pressure_br + buff > up or foot_pressure_br - buff < lp:
        return False

    return True    
    

# Function returns if pose is 90% correct
def check_tree(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    if not check_pressure(data, pd.pressure.MEDIUM):
        return False

def check_warrior1(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    if not check_pressure(data, pd.pressure.MEDIUM):
        return False 

def check_downwardDog(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    data.set_side(pd.limb.HAND)

    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    elif not check_distance(data, pd.limb.HAND, 0, 0, 0, 0):
        return False
    if not check_pressure(data, pd.pressure.HIGH):
        return False 


def check_triangle(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    
    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    if not check_pressure(data, pd.pressure.HIGH):
        return False 
