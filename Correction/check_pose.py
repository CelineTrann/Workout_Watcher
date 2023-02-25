import numpy as np

def check_distance(centroids: list[list], x_distance=0, y_distance=0, tol=5) -> bool:
    arr = np.array(centroids)
    distance = np.ptp(arr, axis=0)
    
    if distance[0] > x_distance + tol or distance[0] < x_distance - tol:
        return False
    elif distance[1] > y_distance + tol or distance[1] < y_distance - tol:
        return False
    
    return True

# Function returns if pose is 90% correct
def check_tree(data: dict[list]) -> bool:
    if not check_distance(data['foot'], 10, 10, 5):
        return False

def check_warrior1(data) -> bool:
    if not check_distance(data['foot'], 10, 10, 5):
        return False

def check_downwardDog(data) -> bool:
    if not check_distance(data['foot'], 10, 10, 5):
        return False
    elif not check_distance(data['hand'], 10, 10, 5):
        return False

def check_triangle(data) -> bool:
    if not check_distance(data['foot'], 10, 10, 5):
        return False
