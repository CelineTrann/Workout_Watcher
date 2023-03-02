from object_detection import process_img
from ImageProcessing.process_data import side
import check_pose as check
import correct_pose as correct
import readData as r

import time

def check_pose(pose, data):
    switch = {
        "tree_right": check.check_tree(data, side.RIGHT),
        "tree_left": check.check_tree(data, side.LEFT),
        "warrior1_right": check.check_warrior1(data, 0, 45),
        "warrior1_left": check.check_warrior1(data, 45, 0),
        "downwardDog": check.check_downwardDog(data),
        "triangle_right": check.check_triangle(data, 0, 90),
        "triangle_left": check.check_triangle(data, 90, 0)
    }

    return switch.get(pose)

def correct_pose(pose, data):
    switch = {
        "tree": correct.correct_tree(data),
        "warrior1_right": correct.correct_warrior1(data, 0, 45),
        "warrior1_left": correct.correct_warrior1(data, 45, 0),
        "downwardDog": correct.correct_downwardDog(data),
        "triangle_right": correct.correct_triangle(data, 0, 90),
        "triangle_left": correct.correct_triangle(data, 90, 0)
    }

    return switch.get(pose)

def choose_pose():
    # bluetooth to get pose
    pose = 'tree'
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
            print('start')
            base = r.readData()
            print('step on mat')
            time.sleep(2)
            data = r.readData()
            
            # Extract Data
            object_list = process_img(base, data)

            if not object_list.is_valid():
                print('Too Many Objects')
                break

            # Check and correct pose
            if not check_pose(pose, object_list):
                correct_pose(pose)
                time.sleep(5)
            else:
                print("Hold Pose.")
                time.sleep(10)

        
if __name__ == "__main__":
    print("working")
    main()
    