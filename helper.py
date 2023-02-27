from ImageProcessing.process_data import Boxes
import numpy as np

def extract_position_data(obj: Boxes) -> dict[list]:
    results = {
        'foot': [],
        'hand': [],
    }
    
    for box in obj.boxes:
        results[f'{box.label}'].append([box.centroid_x, box.centroid_y, box.rotation])

    # if more than hand then consider this data bad
    if len(results['foot']) > 2 or len(results['hand']) > 2:
        return None
    
    return results

def extract_pressure_data(obj: Boxes):
    results = {
        'foot': [],
        'hand': [],
    }

    for box in obj.boxes:
        results[f'{box.label}'].append({
            'ltop': box.ltop_mean,
            'lbottom': box.lbottom_mean,
            'rtop': box.rtop_mean,
            'rbottom': box.rbottom_mean
        })

    return results
