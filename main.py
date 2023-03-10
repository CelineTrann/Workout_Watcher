from object_detection import process_img
from ImageProcessing.process_data import side
import check_pose as check
import correct_pose as correct
import readData as r

import time

import firebase_admin
from firebase_admin import credentials, firestore
import threading
from time import sleep

cred = credentials.Certificate("workoutwatcher-654cd-firebase-adminsdk-xkutc-a7c0fc0bc5.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main tread
callback_done= threading.Event()

boolValue = False

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

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
	for doc in doc_snapshot:
		docDict = doc.to_dict()
		choosePose = docDict['choosePose']
		print(f'Received document snapshot: {doc.id}, choosePose = {choosePose}')
		global boolValue
		boolValue = choosePose
	callback_done.set()
        
    return boolValue

doc_ref = db.collection(u'Poses').document(u'posedoc')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)
while True: 
	print(boolValue)
	sleep(0.5)
        


def main():
    
    while True:
        # Wait for User to Choose Pose
        boolValue = on_snapshot()
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
            print(f'{boolValue}')
            if not check_pose(boolValue, object_list):
                correct_pose(boolValue, object_list)
                time.sleep(5)
            else:
                print("Hold Pose.")
                time.sleep(10)

        
if __name__ == "__main__":
    print("working")
    main()
    