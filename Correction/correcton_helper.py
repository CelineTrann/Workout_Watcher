import numpy as np

def check_distance(centroids: list[list], x_distance=0, y_distance=0, tol=5) -> bool:
    arr = np.array(centroids)
    distance = np.ptp(arr, axis=0)
    
    if distance[0] > x_distance + tol or distance[0] < x_distance - tol:
        return False
    elif distance[1] > y_distance + tol or distance[1] < y_distance - tol:
        return False
    
    return True

def check_angle():
    pass

def check_pressure():
    pass