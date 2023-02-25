from ImageProcessing.process_data import Boxes
import numpy as np

def extract_data(obj: Boxes) -> dict[list]:
    results = {
        'foot': [],
        'hand': [],
    }
    
    for box in obj.boxes:
        results[f'{box.label}'].append([box.centroid_x, box.centroid_y])

    return results


def check_distance(centroids: list[list], x_distance=0, y_distance=0, tol=5) -> bool:
    arr = np.array(centroids)
    distance = np.ptp(arr, axis=0)
    
    if distance[0] > x_distance + tol or distance[0] < x_distance - tol:
        return False
    elif distance[1] > y_distance + tol or distance[1] < y_distance - tol:
        return False
    
    return True

foot = [[6, 2], [3, 4]]
result = check_distance(foot)
print(result)