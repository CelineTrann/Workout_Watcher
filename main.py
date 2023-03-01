from object_detection import process_img
import Correction.check_pose as check
import Correction.correct_pose as correct
import readData as r

import time
import pickle

def check_pose(pose, data):
    switch = {
        "tree": check.check_tree(data),
        "warrior1": check.check_warrior1(data),
        "downwardDog": check.check_downwardDog(data),
        "triangle": check.check_triangle(data)
    }

    return switch.get(pose)

def correct_pose(pose):
    switch = {
        "tree": correct.correct_tree(),
        "warrior1": correct.correct_warrior1(),
        "downwardDog": correct.correct_downwardDog(),
        "triangle": correct.correct_triangle()
    }

    return switch.get(pose)

def choose_pose():
    # bluetooth to get pose
    pose = 'tree'
    return pose

def main():
    # Load ML model
    with open("Model\or3_kneighbour.pkl", 'rb') as file:
        model = pickle.load(file)

    while True:
        # Wait for User to Choose Pose
        pose = choose_pose()
        if pose == 'exit':
            break

        start_pose_time = time.time()
        while time.time() - start_pose_time < 30:
            # Read data from mat
            base = r.readData()
            time.sleep(2)
            data = r.readData()
            
            # Extract Data
            object_list = process_img(base, data, model)

            if not object_list.is_valid():
                break

            # Check and correct pose
            if not check_pose(pose, object_list):
                correct_pose(pose)
                time.sleep(5)
            else:
                print("Hold Pose.")
                time.sleep(10)

        

        


    
