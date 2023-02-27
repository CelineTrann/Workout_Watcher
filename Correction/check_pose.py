import check_helper as cp

# Function returns if pose is 90% correct
def check_tree(data: dict[list], pressure) -> bool:
    lf_desired_pressure = {
        'ltop': 'LOW',
        'lbottom': 'HIGH',
        'rtop': 'HIGH',
        'rbottom': 'HIGH'
    }

    rf_desired_pressure = {
        'ltop': 'HIGH',
        'lbottom': 'HIGH',
        'rtop': 'LOW',
        'rbottom': 'HIGH'
    }

    foot_label = cp.label_side(data['foot'])

    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False
    
    elif not cp.check_angle(data['foot'], 0, 0, 5):
        return False
    
    elif not cp.check_pressure(pressure['foot']):
        return False

    return True

def check_warrior1(data) -> bool:
    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False
    
    elif not cp.check_angle(data['foot'], 0, 45, 5):
        return False

def check_downwardDog(data) -> bool:
    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False
    elif not cp.check_distance(data['hand'], 10, 10, 5):
        return False
    
    elif not cp.check_angle(data['foot'], 0, 0, 5):
        return False
    elif not cp.check_angle(data['hand'], 0, 0, 5):
        return False

def check_triangle(data) -> bool:
    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False
    
    # TODO: determine way to get 90 degrees
    elif not cp.check_angle(data['foot'], 0, 0, 5):
        return False
