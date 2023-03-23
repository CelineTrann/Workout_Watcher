from object_detection import process_img
from ImageProcessing.process_data import side
from gpiozero import Button
import check_pose as check
import correct_pose as correct
import readData as r
import os
import time

import firebase_admin
from firebase_admin import credentials, firestore
import threading
from time import sleep

cred = credentials.Certificate("workoutwatcher-654cd-firebase-adminsdk-xkutc-a7c0fc0bc5.json")
# firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main tread
callback_done= threading.Event()

def check_pose(pose, data) -> bool:
    if pose == "Right Tree Pose": 
        return check.check_tree(data, side.RIGHT)
    elif pose == "Left Tree Pose": 
        return check.check_tree(data, side.LEFT)
    elif pose ==  "Right Warrior 1 Pose": 
        return check.check_warrior1(data, 45, 0)
    elif pose == "Left Warrior 1 Pose": 
        return check.check_warrior1(data, 0, 45)
    elif pose == "downwardDog": 
        return  check.check_downwardDog(data)
    elif pose == "Right Triangle Pose": 
        return  check.check_triangle(data, 90, 0)
    elif pose ==  "Left Triangle Pose": 
        return  check.check_triangle(data, 0, 90)
 
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

doc_ref = db.collection(u'users').document(u'1y8SFUDXOZbx03bxUPRlXPkvgeq1')


def main():
    
    print("waiting for network configuration.")
#     time.sleep(30)
    
#     shut_But = Button(4)
#     
#     while True:
#        if shut_But.is_pressed:
# #            os.system("sudo poweroff")
#            time.sleep(1)
#            print("Button pressed.")
#        else:
#            print("Waiting for button press.")
    
    prev_pose = ""
    pose = None
    while True:
        # Wait for User to Choose Pose
        doc_ref = db.collection(u'users').document(u'1y8SFUDXOZbx03bxUPRlXPkvgeq1')
        while pose == None:
            doc_ref.on_snapshot(on_snapshot)
            ref = doc_ref.get()
            pose = ref.get("poseSelected")
            time.sleep(0.5)
            print(pose)
                    
        if pose == 'exit':
            break
        else:
            doc_ref = db.collection('users').document('1y8SFUDXOZbx03bxUPRlXPkvgeq1')
            doc_ref.update({
            'isPoseCorrect': False
            })
            
        start_pose_time = time.time()
        while time.time() - start_pose_time < 30:
            # Read data from mat
            # TODO: check if person is off mat (Murphy)
            print('Please step off the mat.')
            time.sleep(2)
            base = r.readData()
            print('step on mat')
            time.sleep(7)
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