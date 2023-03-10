import firebase_admin
from firebase_admin import credentials, firestore
import threading
from time import sleep

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create an Event for notifying main tread
callback_done= threading.Event()

boolValue = False

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
	for doc in doc_snapshot:
		docDict = doc.to_dict()
		isTrue = docDict['isTrue']
		print(f'Received document snapshot: {doc.id}, isTrue = {isTrue}')
		global boolValue
		boolValue = isTrue
	callback_done.set()

doc_ref = db.collection(u'testC').document(u'testD')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)
while True: 
	print(boolValue)
	sleep(0.5)
	