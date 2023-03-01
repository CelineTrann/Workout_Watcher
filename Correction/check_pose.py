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

# Function returns if pose is 90% correct
def check_tree(data: pd.Boxes) -> bool:
    objs = data.no_label
    if len(objs) > 1:
        return False
    
    objs[0].set_label(pd.limb.FOOT.value)
    data.set_side(pd.limb.FOOT)

    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False

def check_warrior1(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False

def check_downwardDog(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    data.set_side(pd.limb.HAND)

    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
    elif not check_distance(data, pd.limb.HAND, 0, 0, 0, 0):
        return False

def check_triangle(data: pd.Boxes) -> bool:
    data.set_side(pd.limb.FOOT)
    
    if not check_distance(data, pd.limb.FOOT, 0, 0, 0, 0):
        return False
