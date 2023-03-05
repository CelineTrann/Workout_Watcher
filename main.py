from object_detection import process_img
from ImageProcessing.process_data import side
import check_pose as check
import correct_pose as correct
import readData as r

import time

def check_pose(pose, data) -> bool:
    if pose == "tree_right": 
        return check.check_tree(data, side.RIGHT)
    elif pose == "tree_left": 
        return check.check_tree(data, side.LEFT)
    elif pose ==  "warrior1_right": 
        return check.check_warrior1(data, 0, 45)
    elif pose == "warrior1_left": 
        return check.check_warrior1(data, 45, 0)
    elif pose == "downwardDog": 
        return  check.check_downwardDog(data)
    elif pose == "triangle_right": 
        return  check.check_triangle(data, 0, 90)
    elif pose ==  "triangle_left": 
        return  check.check_triangle(data, 90, 0)
 
    return False

def correct_pose(pose, data) -> None:
    if pose == "tree_right": 
        correct.correct_tree(data, side.RIGHT)
    elif pose == "tree_left": 
        correct.correct_tree(data, side.LEFT)
    elif pose == "warrior1_right": 
        correct.correct_warrior1(data, 0, 45)
    elif pose == "warrior1_left": 
        correct.correct_warrior1(data, 45, 0)
    elif pose == "downwardDog": 
        correct.correct_downwardDog(data)
    elif pose == "triangle_right": 
        correct.correct_triangle(data, 0, 90)
    elif pose == "triangle_left": 
        correct.correct_triangle(data, 90, 0)

def choose_pose():
    # bluetooth to get pose
    pose = 'tree_right'
    return pose

def main():
    
    while True:
        # Wait for User to Choose Pose
        pose = choose_pose()
        if pose == 'exit':
            break

        start_pose_time = time.time()
        while time.time() - start_pose_time < 30:
            # Read data from mat
            # TODO: check if person is off mat (Murphy)
            print('Please step off the mat.')
            time.sleep(2)
            base = r.readData()
            print('step on mat')
            time.sleep(5)
            data = r.readData()
            
            # Extract Data
            object_list = process_img(base, data)

            if not object_list.is_valid():
                print('Too Many Objects')
                break

            # Check and correct pose
            print(f'{pose}')
            if not check_pose(pose, object_list):
                correct_pose(pose, object_list)
                time.sleep(5)
            else:
                print("Hold Pose.")
                time.sleep(10)

        
if __name__ == "__main__":
    print("working")
    main()
    