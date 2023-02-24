import pickle
from object_detection import process_img

def main():
    # Load ML model
    with open("or_kneighbour.pkl", 'rb') as file:
        model = pickle.load(file)

    # While On:
        # Wait for User to Choose Pose

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

        # if not continue:
            # send result to phone
            # break
        


    
