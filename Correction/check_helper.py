import numpy as np

def check_distance(centroids: list[list], x_distance, y_distance, tol=5) -> bool:
    '''
    postion -- [centroid_x, centroid_y, rotationt] of an object
    x_distance -- desired distance between object on x-axis
    y_distance -- desired distance between object on y-axis
    tol -- tolerance
    '''
    arr = np.array(centroids)
    distance = np.ptp(arr, axis=0)
    
    if distance[0] > x_distance + tol or distance[0] < x_distance - tol:
        return False
    elif distance[1] > y_distance + tol or distance[1] < y_distance - tol:
        return False
    
    return True

def check_angle(position: list, desired_rot1, desired_rot2, tol) -> bool:
    '''
    postion -- [centroid_x, centroid_y, rotationt] of an object
    desired_rot1 -- rotation of one object on mat
    desired_rot2 -- reotation of other object on mat
    tol -- allowed tolerance from desired angles
    '''
    if not any(rot[2] >= desired_rot1 - tol and rot[2] <= desired_rot1 + tol for rot in position):
        return False
        
    elif not any(rot[2] >= desired_rot2 - tol and rot[2] <= desired_rot2 + tol for rot in position):
        return False

    return True

def check_pressure(pressure: dict, desired_pressure: dict):
    for key in pressure:
        if pressure[key] != desired_pressure[key]:
            return False
    
    return True