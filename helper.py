from ImageProcessing.process_data import Boxes
import numpy as np

def extract_centroid_data(obj: Boxes) -> dict[list]:
    results = {
        'foot': [],
        'hand': [],
    }
    
    for box in obj.boxes:
        results[f'{box.label}'].append([box.centroid_x, box.centroid_y])

    return results
