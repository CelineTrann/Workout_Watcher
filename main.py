import Correction.check_pose as check
import Correction.correct_pose as correct
from object_detection import process_img

import pickle

def check_pose(pose):
    switch = {
        "tree": check.check_tree(),
        "warrior1": check.check_warrior1(),
        "downwardDog": check.check_downwardDog(),
        "triangle": check.check_triangle()
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

def main():
    # Load ML model
    with open("or_kneighbour.pkl", 'rb') as file:
        model = pickle.load(file)

    # While On:
        # Wait for User to Choose Pose
        pose = "tree"

        holding_pose = True
        while holding_pose:
            # Get data from mat
            base = 0
            data = 0
            
            # process and clean data
            # process data image and get data from object
            # classify object
            # compile data (object type, location, rotation, pressure regions) 
            object_list = process_img(base, data, model)

            # Check and correct posture
            if not check_pose(pose):
                correct_pose(pose)


        # if not continue:
            # send result to phone
            # break
        


    
