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

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
	for doc in doc_snapshot:
		docDict = doc.to_dict()
		poseSelected = docDict['poseSelected']
		print(f'Received document snapshot: {doc.id}, poseSelected = {poseSelected}')
		global boolValue
		boolValue = poseSelected
	callback_done.set()

doc_ref = db.collection(u'users').document(u'Oxh3TSSqc1YUcuLIgc6ggw0y3ib2')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)
while True: 
	print(boolValue)
	sleep(0.5)
	