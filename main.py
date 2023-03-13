from object_detection import process_img
from ImageProcessing.process_data import side
import check_pose as check
import correct_pose as correct
import readData as r
#import cv2 as cv

import time

import firebase_admin
from firebase_admin import credentials, firestore
import threading
from time import sleep

cred = credentials.Certificate("workoutwatcher-654cd-firebase-adminsdk-xkutc-a7c0fc0bc5.json")
#firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main tread
callback_done= threading.Event()


def check_pose(pose, data) -> bool:
    if pose == "tree_right": 
        return check.check_tree(data, side.RIGHT)
    elif pose == "tree_left": 
        return check.check_tree(data, side.LEFT)
    elif pose ==  "warrior1_right": 
        return check.check_warrior1(data, 45, 0)
    elif pose == "warrior1_left": 
        return check.check_warrior1(data, 0, 45)
    elif pose == "downwardDog": 
        return  check.check_downwardDog(data)
    elif pose == "triangle_right": 
        return check.check_triangle(data, 0, 90)
    elif pose ==  "triangle_left": 
        return  check.check_triangle(data, 90, 0)
 
    return False


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        docDict = doc.to_dict()
        poseSelected = docDict["poseSelected"]
        print(
            f"Received document snapshot: {doc.id}, poseSelected = {poseSelected}"
        )
        global pose
        pose = poseSelected
    callback_done.set()

    return pose

doc_ref = db.collection(u'users').document(u'Oxh3TSSqc1YUcuLIgc6ggw0y3ib2')


def main():
    
    prev_pose = ""
    while True:
        # Wait for User to Choose Pose
        doc_ref.on_snapshot(on_snapshot)
        ref = doc_ref.get()
        pose = ref.get("poseSelected")
                    
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
            check_pose(pose, object_list)

        
if __name__ == "__main__":
    print("working")
    main()