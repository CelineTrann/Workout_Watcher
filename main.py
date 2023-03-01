from object_detection import process_img
import check_pose as check
import correct_pose as correct

import pickle
import time

def check_pose(pose, data):
    switch = {
        "tree": check.check_tree(data),
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

def main():
    # Load ML model
    with open("Model\or3_kneighbour.pkl", 'rb') as file:
        model = pickle.load(file)

    On = True
    while On:
        # Wait for User to Choose Pose
        pose = "tree"

        if pose == 'exit':
            # send result to phone
            return

        start_time = time.time()
        while time.time() - start_time < 20:
            # Get data from mat
            base = 0
            data = 0
            
            # process and clean data
            # process data image and get data from object
            # classify object
            # compile data (object type, location, rotation, pressure regions) 
            object_list = process_img(base, data, model)

            if not object_list.is_valid():
                break

            if not check_pose(pose, object_list):
                correct_pose(pose)
            else:
                # wait 5 seconds before checking pose again
                time.sleep(5)

        
if __name__ == "__main__":
    print("working")
    main()
    