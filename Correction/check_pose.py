import correcton_helper as cp

# Function returns if pose is 90% correct
def check_tree(data: dict[list]) -> bool:
    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False

def check_warrior1(data) -> bool:
    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False

def check_downwardDog(data) -> bool:
    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False
    elif not cp.check_distance(data['hand'], 10, 10, 5):
        return False

def check_triangle(data) -> bool:
    if not cp.check_distance(data['foot'], 10, 10, 5):
        return False
